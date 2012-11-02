from behave import when
from behaving.personas.persona import persona_vars


@when(u'I click the link to "{url}"')
@persona_vars
def click_link_to_url(context, url):
    context.browser.click_link_by_href(url)


@when(u'I click the link to a url that contains "{url}"')
@persona_vars
def click_link_to_url_that_contains(context, url):
    context.browser.click_link_by_partial_href(url)


@when(u'I click the link with text "{text}"')
@persona_vars
def click_link_with_text(context, text):
    context.browser.click_link_by_text(text)


@when(u'I click the link with text that contains "{text}"')
@persona_vars
def click_link_with_text_that_contains(context, text):
    context.browser.click_link_by_partial_text(text)
