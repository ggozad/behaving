from behave import when, then
from splinter.browser import Browser

from behaving.personas.persona import persona_vars


@when(u'I visit "{url}"')
@when(u'I go to "{url}"')
def when_i_visit_url(context, url):
    if not context.browser:
        context.browser = Browser()
    context.browser.visit(url)


@then(u'the browser\'s URL should be "{url}"')
def the_browser_url_should_be(context, url):
    assert context.browser.url.strip() == url, 'Expected %s but got %s' % (url, context.browser.url)


@then(u'the browser\'s URL should contain "{text}"')
@persona_vars
def the_browser_url_should_contain(context, text):
    assert text in context.browser.url


@then(u'the browser\'s URL should not contain "{text}"')
@persona_vars
def the_browser_url_should_not_contain(context, text):
    assert text not in context.browser.url
