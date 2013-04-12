from behave import step
from splinter.browser import Browser
from urlparse import urljoin

from behaving.personas.persona import persona_vars


@step(u'the base url "{url}"')
def given_the_base_url(context, url):
    context.base_url = url


@step(u'I visit "{url}"')
@step(u'I go to "{url}"')
def when_i_visit_url(context, url):
    full_url = urljoin(context.base_url, url)
    if not context.browser:
        context.browser = Browser()
    context.browser.visit(full_url)


@step(u'the browser\'s URL should be "{url}"')
def the_browser_url_should_be(context, url):
    full_url = urljoin(context.base_url, url)
    assert context.browser.url.strip() == full_url, 'Expected %s but got %s' % (full_url, context.browser.url)


@step(u'the browser\'s URL should contain "{text}"')
@persona_vars
def the_browser_url_should_contain(context, text):
    assert text in context.browser.url


@step(u'the browser\'s URL should not contain "{text}"')
@persona_vars
def the_browser_url_should_not_contain(context, text):
    assert text not in context.browser.url
