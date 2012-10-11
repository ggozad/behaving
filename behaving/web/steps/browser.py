from behave import given, when
from splinter.browser import Browser


@given(u'a browser')
def given_a_browser(context):
    if hasattr(context, 'browser'):
        context.browser.quit()
    if context.default_browser:
        context.browser = Browser(context.default_browser)
    else:
        context.browser = Browser()


@given(u'{brand} as the browser')
def given_some_browser(context, brand):
    brand = brand.lower()
    assert brand in [u'firefox', u'chrome'], u'You can only use Firefox or Chrome as a browser'
    if hasattr(context, 'browser'):
        context.browser.quit()
    context.default_browser = brand
    context.browser = Browser(brand)


@when(u'I reload')
def reload(context):
    context.browser.reload()


@when(u'I go back')
def go_back(context):
    context.browser.back()


@when(u'I go forward')
def go_forward(context):
    context.browser.forward()
