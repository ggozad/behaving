from behave import when

from behaving.personas.persona import persona_vars


@when('I click the link to "{url}"')
@persona_vars
def click_link_to_url(context, url):
    el = context.browser.links.find_by_href(url).first
    assert el, f"Link {url} not found"
    el.click()


@when('I click the link to a url that contains "{url}"')
@persona_vars
def click_link_to_url_that_contains(context, url):
    el = context.browser.links.find_by_partial_href(url).first
    assert el, f"Link containing {url} not found"
    el.click()


@when('I click the link with text "{text}"')
@persona_vars
def click_link_with_text(context, text):
    el = context.browser.links.find_by_text(text).first
    assert el, f"Link containing {text} not found"
    el.click()


@when('I click the link with text that contains "{text}"')
@persona_vars
def click_link_with_text_that_contains(context, text):
    text = text.replace('"', '\\"')  # Escape all double quotes
    text = text.replace("'", """', "'", '""")  # Escape all single quotes
    if "'" in text:
        xpath = f"//a[contains(string(), concat('{text}'))]"
    else:
        xpath = f"//a[contains(string(), '{text}')]"
    anchor = context.browser.find_by_xpath(xpath).first
    assert anchor, f"Link containing {text} not found"
    anchor.click()
