import os
try:
    from urllib2 import URLError
except ImportError:
    from urllib.error import URLError

# Generic setup/teardown for compatibility with pytest et al.


def setup(context):
    if not hasattr(context, 'default_browser'):
        context.default_browser = ''
    if not hasattr(context, 'browser_args'):
        context.browser_args = {}
    if not hasattr(context, 'remote_webdriver'):
        context.remote_webdriver = False
    if not hasattr(context, 'attachment_dir'):
        context.attachment_dir = '/'
    if not hasattr(context, 'base_url'):
        context.base_url = ''
    if not hasattr(context, 'default_browser_size'):
        context.default_browser_size = None
    if hasattr(context, 'screenshots_dir'):
        if not os.path.isdir(context.screenshots_dir):
            try:
                os.mkdir(context.screenshots_dir)
            except OSError:
                context.screenshots_dir = ''
    else:
        context.screenshots_dir = ''

    context.browser = None
    context.browsers = {}


def teardown(context):
    for browser in context.browsers.values():
        try:
            browser.quit()
        except URLError:
            pass

    context.browser = None
    context.browsers = {}
