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
    text = text.replace('"', '\\"')  # Escape all double quotes
    text = text.replace("'", """', "'", '""")  # Escape all single quotes
    if "'" in text:
        xpath = "//a[contains(string(), concat('%s'))]" % text
    else:
        xpath = "//a[contains(string(), '%s')]" % text
    anchors = context.browser.find_by_xpath(xpath)
    assert anchors, "Link not found"
    anchors[0].click()
