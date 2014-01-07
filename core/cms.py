# -*- encoding: utf-8 -*-
from simplecms.registry import set_snippet_settings, add_dashboard_pane
from simplecms import panes
from simplecms.registry import add_template
from simplecms.template import Template, TemplateBlock


def setup():
    set_snippet_settings("imagesnippet", "sizes", [
        (100, 100, True, "thumb"),
        (400, 400, True, "content"),
        (200, 200, True, "content_small"),
    ])

    set_snippet_settings("imagesnippet", "content_sizes", [
        ('content', u"groß"),
        ('content_small', u"klein"),
    ])

    set_snippet_settings("imagesnippet", "styles", [
        ("float_left", "Links, vom Text umflossen"),
        ("float_right", "Rechts, vom Text umflossen"),
        ("block", "Nicht umflossen"),
    ])

    set_snippet_settings("textsnippet", "styles", [
        ("pull_quote", "Pull Quote"),
        ("right", "Right"),
    ])

    set_snippet_settings("videosnippet", "width", 320)
    set_snippet_settings("videosnippet", "height", 240)

    add_dashboard_pane(panes.PagesDashboardPane())

    t = Template(name="Default",
                 slug="default",
                 desc="default template",
                 path="content.html")
    t.add_block(TemplateBlock(name="content", slug="content"))
    add_template(t)
