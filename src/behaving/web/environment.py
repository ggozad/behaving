from urllib2 import URLError


def before_all(context):
    if not hasattr(context, 'default_browser'):
        context.default_browser = ''
    if not hasattr(context, 'attachment_dir'):
        context.attachment_dir = '/'
    if not hasattr(context, 'base_url'):
        context.base_url = ''

    # Disable logging, selenium tends to be pretty verbose
    context.config.log_capture = False


def before_feature(context, feature):
    pass


def before_scenario(context, scenario):
    context.browser = None
    context.browsers = dict()


def after_feature(context, feature):
    pass


def after_scenario(context, scenario):
    for browser in context.browsers.values():
        try:
            browser.quit()
        except URLError:
            pass

    if context.browser is not None:
        try:
            context.browser.quit()
        except URLError:
            pass


def after_all(context):
    pass
