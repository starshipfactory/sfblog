# -*- encoding: utf-8 -*-
"""
Import from s9y RSS export

Warning: this is specifically written for

https://starship-factory.ch/rss.php?version=2.0&all=1

and is pretty much a one-off script. Don't expect it to work on
other RSS feeds, it might not work or break your site/eat your babies/...

"""
import os
import re
import sys
import json
import time
import rfc822
import hashlib
import urlparse
import datetime
from contextlib import contextmanager
import requests
from lxml import objectify, html, etree
from lxml.html.clean import clean_html

from django.db import transaction
from django.utils.html import escape
from django.utils.text import slugify
from django.utils.timezone import make_aware, utc
from django.core.files.images import ImageFile
from django.contrib.sites.models import Site
from django.contrib.redirects.models import Redirect

from simplecms.models import TextSnippet, ImageSnippet, Content
from zinnia.models.entry import Entry
from zinnia.models.category import Category

_url_cache = {}


def my_slugify(value):
    """
    slugify with umlauts
    """
    translation_table = {
        u'ß': 'ss',
        u'ä': 'ae',
        u'ö': 'oe',
        u'ü': 'ue',
        u'é': 'e',
        u'Ä': 'Ae',
        u'Ö': 'Oe',
        u'Ü': 'Ue',
        u'É': 'E',
    }
    for k, v in translation_table.items():
        value = value.replace(k, v)
    return slugify(value)


def follow_redirects(url, verify=True):
    """
    follow any redirects and return the resulting url
    """
    s = requests.Session()
    s.max_redirects = 10  # FIXME: magic number...
    s.verify = verify
    try:
        resp = s.head(url, allow_redirects=True)
    except requests.exceptions.SSLError, e:
        if verify:
            return follow_redirects(url, verify=False)
        else:
            print >> sys.stderr, e, url
            return url
    except requests.exceptions.ConnectionError, e:
        print >> sys.stderr, e, url
        return url
    return resp.url


def transform_image_url(url):
    """
    rewrite the url to the image to one that is closer to the original size
    """
    from django.utils.http import urlencode
    url = url.replace("serendipityThumb.", "")
    if "admin_image_selector.php" in url:
        width_key = 'serendipity[resizeWidth]'
        height_key = 'serendipity[resizeHeight]'
        parsed_url = urlparse.urlparse(url)
        qs = parsed_url.query
        parsed_qs = urlparse.parse_qs(qs)

        if height_key in parsed_qs:
            parsed_qs[height_key] = "10000"
        if width_key in parsed_qs:
            parsed_qs[width_key] = "10000"

        qs = urlencode(parsed_qs, doseq=1)
        url = parsed_url._replace(query=qs).geturl()
    return url


def add_redirect(full_old_url, new_path):
    """
    add a redirect entry. for example
    full_old_url=http://example.org/blog/post1/
    new_path=/2014/05/06/post1/
    """
    current_site = Site.objects.get_current()
    parsed_old = urlparse.urlparse(full_old_url)
    if parsed_old.query:
        # bail out: can only handle paths
        return
    # theres a unique constraint on (site_id, old_path), so get rid of old redirects
    Redirect.objects.filter(site=current_site,
                            old_path=parsed_old.path).delete()
    Redirect.objects.get_or_create(site=current_site,
                                   old_path=parsed_old.path,
                                   new_path=new_path)


def image_cache_path(url):
    key = hashlib.md5(url).hexdigest()
    if not os.isdir("image_cache"):
        os.mkdir("image_cache")
    return os.path.join("image_cache", key)


def image_cache_get(url):
    """
    get a file handle for the image at ``url``
    """
    path = image_cache_path(url)
    if os.path.exists(path):
        return open(path)


@contextmanager
def image_cache_put(url):
    path = image_cache_path(url)
    fp = open(path, "wb")
    yield fp
    fp.close()


def fetch_image(url):
    url = transform_image_url(url)
    img = image_cache_get(url)
    if img:
        return img
    resp = requests.get(url, stream=True)
    if resp.status_code == 200:
        with image_cache_put(url) as fp:
            for chunk in resp.iter_content(1024):
                fp.write(chunk)
    return image_cache_get(url)


def resolve_url(url):
    if url in _url_cache:
        return _url_cache[url]
    dest_url = follow_redirects(url)
    _url_cache[url] = dest_url
    return dest_url


class HTMLWalker(object):
    """
    walk an element tree; when encountering an image, save the elements encountered
    from ``self.current_snippet`` into ``self.snippets`` and start a new snippet.
    """
    self_closing = ["img"]

    def __init__(self):
        self.current_snippet = []
        self.snippets = []
        self.current_type = "text"

    def add(self, blob):
        self.current_snippet.append(blob)

    def done(self, new_type="text"):
        self.snippets.append((self.current_type, self.current_snippet))
        self.current_type = new_type
        self.current_snippet = []

    def walk(self, elem, indent=0, stack=None):
        stack = stack or []
        space = indent * 4 * " "
        space = ""

        if elem.tag == "img":
            if "src" not in elem.attrib:
                return
            # close any open tags
            for e in list(reversed(stack))[1:]:
                self.add("%s</%s>" % (space, e.tag,))
            self.done(new_type="image")

        # special case: thumbnail linked to the full image
        if elem.tag == "a" and elem.attrib.get("class", "") == "serendipity_image_link":
            self.done(new_type="image")
            title = elem.find("img").attrib.get("title", "")
            self.add("<img src='%s' alt='%s' title='%s' />" %
                     (elem.attrib.get("href"),
                      title, title))
            self.done()
            return

        if elem.tag == "div" and len(elem.xpath("//*")) == 0:
            return

        if elem.attrib:
            attrs = " " + " ".join('%s="%s"' % (escape(k), escape(v))
                                   for k, v in elem.attrib.items())
        else:
            attrs = ""

        if elem.tag in self.self_closing:
            self.add("%s<%s%s />" % (space, elem.tag, attrs))
        else:
            self.add("%s<%s%s>" % (space, elem.tag, attrs))

        for child in elem.xpath("./text()|./node()"):
            if isinstance(child, basestring):
                self.add("%s%s" % (space, child))
            else:
                self.walk(child, indent + 1, stack + [child])
        if elem.tag not in self.self_closing:
            self.add("%s</%s>" % (space, elem.tag))

        if elem.tag == "img":
            self.done()
            # re-open previously closed tags
            for e in stack[:-1]:
                self.add("%s<%s>" % (space, e.tag,))


def node_has_children(elem):
    if elem.xpath("./*"):
        return True
    text_nodes = elem.xpath("./text()")
    text_nodes = [t.strip() for t in text_nodes]
    if any(text_nodes):
        return True
    return False


def postprocess_html_snippet(blob):
    """
    remove empty paragraphs, fix links, ...
    """
    blob = blob.strip()
    if not blob:
        return blob
    try:
        root = html.fromstring(blob)
    except etree.ParserError, e:
        print >> sys.stderr, e
        print >> sys.stderr, repr(blob.encode("utf8"))
        return blob
    for p in root.xpath("//p"):
        if not node_has_children(p):
            p.getparent().remove(p)
    for div in root.xpath("//div"):
        if not node_has_children(div):
            div.getparent().remove(div)
    for a in root.xpath("//a"):
        if not 'href' in a.attrib:
            continue
        orig_href = a.attrib['href']
        if "exit.php" in orig_href or "archive" in orig_href:
            a.attrib['href'] = resolve_url(orig_href)
    return html.tostring(root)


def process_image_html_blob(blob):
    root = html.fromstring(blob)
    img = root.xpath("//img")[0]
    src = img.attrib['src']
    fp = fetch_image(src)
    return fp, {"title": img.attrib.get("title", "") or img.attrib.get("alt", "")}


def image_extension(fp):
    from PIL import Image
    i = Image.open(fp)
    return i.format.lower()


def process_html_blob(blob, cms_content):
    # - h1, h2 need to be mapped to h3, h4 (only one blog post affected, so do manually)
    # - need to handle url mapping
    #   old: https://starship-factory.ch/archives/27-Starship-Factory-heute-n....html
    #   new: /2014/05/01/Starship-Factory-heute-nachmittag-geoeffnet/
    root = html.fromstring(clean_html(blob))

    walker = HTMLWalker()
    walker.walk(root)
    walker.done()

    order = 0
    for snippet_type, snippet in walker.snippets:
        joined = "".join(snippet)
        if not joined.strip():
            continue
        processed = postprocess_html_snippet(joined).encode("utf8")
        if snippet_type == "text":
            ts = TextSnippet()
            ts.content = cms_content
            ts.order = order
            ts.body = processed
            ts.block_slug = "content"
            ts.save()
        if snippet_type == "image":
            fp, img_attrs = process_image_html_blob(processed)
            ext = image_extension(fp)
            isnippet = ImageSnippet()
            isnippet.content = cms_content
            isnippet.order = order
            isnippet.title = unicode(img_attrs['title']) or unicode(fp.name)
            image_filename = "%s.%s" % (my_slugify(isnippet.title), ext)
            isnippet.size = 'content'
            isnippet.image = ImageFile(fp, name=image_filename)
            isnippet.block_slug = "content"
            isnippet.save()
        order += 1


def parse_rss_date(date_as_str):
    dt = datetime.datetime.fromtimestamp(time.mktime(rfc822.parsedate(date_as_str)))
    return make_aware(dt, utc)


@transaction.atomic
def import_from_rss(rss_as_bytes):
    rss = objectify.fromstring(rss_as_bytes)
    current_site = Site.objects.get_current()
    for item in rss.channel.item:
        blob = unicode(item['{%s}encoded' % item.nsmap['content']])
        category, _ = Category.objects.get_or_create(
            slug=my_slugify(unicode(item.category.text)),
            title=unicode(item.category.text)
        )

        entry = Entry()
        cms_content = Content()
        cms_content.save()
        process_html_blob(blob, cms_content)
        entry.content_ptr = cms_content
        entry.title = unicode(item.title.text)
        entry.creation_date = parse_rss_date(unicode(item.pubDate))
        entry.slug = my_slugify(entry.title)
        entry.save()
        entry.sites.add(current_site)
        entry.categories.add(category)
        link = unicode(item.link.text)
        _url_cache[link] = entry.get_absolute_url()
        _url_cache[re.sub("^https", "http", link)] = entry.get_absolute_url()
        add_redirect(link, entry.get_absolute_url())


def main(url_or_fname):
    global _url_cache
    if os.path.exists("url_cache.json"):
	with open("url_cache.json") as fp:
		_url_cache = json.load(fp)

    try:
        if url_or_fname.startswith('http'):
            resp = requests.get(url_or_fname)
            import_from_rss(resp.content)
        else:
            import_from_rss(open(url_or_fname).read())
    finally:
        with open("url_cache.json", "w") as fp:
            json.dump(_url_cache, fp)

if __name__ == "__main__":
    main(sys.argv[1])
