import os
import tempfile
from urllib.error import URLError

from behaving.web import electron
from behaving.web import chrome
from behaving.web import firefox


# Generic setup/teardown for compatibility with pytest et al.
def setup(context):
    if not hasattr(context, "default_browser"):
        context.default_browser = ""
    if not hasattr(context, "browser_args"):
        context.browser_args = {}
    if not hasattr(context, "attachment_dir"):
        context.attachment_dir = "/"
    if not hasattr(context, "base_url"):
        context.base_url = ""
    if not hasattr(context, "default_browser_size"):
        context.default_browser_size = None
    if not hasattr(context, "max_browser_attempts"):
        context.max_browser_attempts = 3
    if hasattr(context, "screenshots_dir"):
        if not os.path.isdir(context.screenshots_dir):
            try:
                os.mkdir(context.screenshots_dir)
            except OSError:
                context.screenshots_dir = ""
    else:
        context.screenshots_dir = ""
    if not hasattr(context, "remote_webdriver_url"):
        context.remote_webdriver_url = ""

    # Setup download path
    if not hasattr(context, "download_dir"):
        context.download_dir = tempfile.mkdtemp()
        chrome._DOWNLOAD_PATH = context.download_dir
        firefox._DOWNLOAD_PATH = context.download_dir

    context.browsers = {}


def teardown(context):
    for browser in context.browsers.values():
        try:
            browser.quit()
        except URLError:
            pass
    if hasattr(context, "browser"):
        del context.browser
    if hasattr(context, "browsers"):
        context.browsers.clear()
