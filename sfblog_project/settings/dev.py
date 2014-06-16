from .base import *  # NOQA

SERVE_STATIC_FILES = True

try:
    import debug_toolbar  # NOQA

    INSTALLED_APPS += (
        'debug_toolbar',
    )

    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    )

    DEBUG_TOOLBAR_PATCH_SETTINGS = False

    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": set([
            'debug_toolbar.panels.redirects.RedirectsPanel',
            'debug_toolbar.panels.sql.SQLPanel',
        ])
    }
except ImportError:
    pass


try:
    import debug_toolbar  # NOQA
    import debug_toolbar_line_profiler  # NOQA

    INSTALLED_APPS += (
        'debug_toolbar_line_profiler',
    )

    DEBUG_TOOLBAR_PANELS += (
        'debug_toolbar_line_profiler.panel.ProfilingPanel',
    )
except ImportError:
    pass

INTERNAL_IPS = ('127.0.0.1', '::1')
