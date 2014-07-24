try:
    from urlparse import urljoin, urlparse
except ImportError:
    from urllib.parse import urljoin, urlparse
from behave import step
import parse

from behaving.personas.persona import persona_vars


@step(u'the base url "{url}"')
def given_the_base_url(context, url):
    context.base_url = url


@step(u'I visit "{url}"')
@step(u'I go to "{url}"')
@persona_vars
def when_i_visit_url(context, url):
    full_url = urljoin(context.base_url, url)
    context.browser.visit(full_url)


@step(u'the browser\'s URL should be "{url}"')
@persona_vars
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


@step(u'I parse the url path and set "{expression}"')
@persona_vars
def parse_sms_set_var(context, expression):
    assert context.persona is not None, u'no persona is setup'
    url = urlparse(context.browser.url).path
    parser = parse.compile(expression)
    res = parser.parse(url)
    assert res, u'expression not found'
    assert res.named, u'expression not found'
    for key, val in res.named.items():
        context.persona[key] = val
