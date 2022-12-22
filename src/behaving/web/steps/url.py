from urllib.parse import urljoin, urlparse

from behave import given, then, when

from behaving.personas.persona import persona_vars
from behaving.utils import parse_text


@given('the base url "{url}"')
def given_the_base_url(context, url):
    context.base_url = url


@when('I visit "{url}"')
@when('I go to "{url}"')
@persona_vars
def when_i_visit_url(context, url):
    full_url = urljoin(context.base_url, url)
    context.browser.visit(full_url)


@then('the browser\'s URL should be "{url}"')
@persona_vars
def the_browser_url_should_be(context, url):
    full_url = urljoin(context.base_url, url)
    assert (
        context.browser.url.strip() == full_url
    ), f"Expected {full_url} but got {context.browser.url}"


@then('the browser\'s URL should contain "{text}"')
@persona_vars
def the_browser_url_should_contain(context, text):
    assert text in context.browser.url, f'"{text}" not found in {context.browser.url}'


@then('the browser\'s URL should not contain "{text}"')
@persona_vars
def the_browser_url_should_not_contain(context, text):
    assert text not in context.browser.url, f'"{text}" found in {context.browser.url}'


@when('I parse the url path and set "{expression}"')
@persona_vars
def parse_url_set_var(context, expression):
    assert context.persona is not None, "No persona is setup"
    url = urlparse(context.browser.url).path
    parse_text(context, url, expression)
