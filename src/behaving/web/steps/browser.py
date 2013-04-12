from behave import step
from splinter.browser import Browser


@step(u'a browser')
def given_a_browser(context):
    named_browser(context, '')


@step(u'browser "{name}"')
def named_browser(context, name):
    if name not in context.browsers:
        if context.default_browser:
            context.browsers[name] = Browser(context.default_browser)
        else:
            context.browsers[name] = Browser()
    context.browser = context.browsers[name]
    context.browser.switch_to_window(context.browser.windows[0])


@step(u'{brand} as the default browser')
def given_some_browser(context, brand):
    brand = brand.lower()
    assert brand in [u'firefox', u'chrome', u'phantomjs', 'remote'], u'Unknown browser'
    context.default_browser = brand


@step(u'I reload')
def reload(context):
    context.browser.reload()


@step(u'I go back')
def go_back(context):
    context.browser.back()


@step(u'I go forward')
def go_forward(context):
    context.browser.forward()
