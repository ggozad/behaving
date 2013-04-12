from behave import step
from behaving.personas.persona import persona_vars


@step(u'I click the link to "{url}"')
@persona_vars
def click_link_to_url(context, url):
    context.browser.click_link_by_href(url)


@step(u'I click the link to a url that contains "{url}"')
@persona_vars
def click_link_to_url_that_contains(context, url):
    context.browser.click_link_by_partial_href(url)


@step(u'I click the link with text "{text}"')
@persona_vars
def click_link_with_text(context, text):
    context.browser.click_link_by_text(text)


@step(u'I click the link with text that contains "{text}"')
@persona_vars
def click_link_with_text_that_contains(context, text):

    # Thought the following search by xpath should work
    # find_by_xpath("//a[contains(text(), '%s')]" % text)
    # but it doesn't.
    # The following is a workaround
    anchors = context.browser.find_link_by_partial_text(text) or \
        [a for a in context.browser.find_by_tag('a') if text in a.text]

    assert anchors, 'Link not found'
    anchors[0].click()
