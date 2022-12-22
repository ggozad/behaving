from behave import when
from splinter.exceptions import ElementDoesNotExist


@when('I set "{key}" to the text of "{name}"')
def set_key_to_el_text(context, key, name):
    assert context.persona is not None, "no persona is setup"
    el = context.browser.find_by_xpath(
        ("//*[@id='%(name)s']|" "//*[@name='%(name)s']") % {"name": name}
    )
    assert el, f"Element with id or name {name} not found"
    context.persona[key] = el.first.text


@when('I set "{key}" to the attribute "{attr}" of the element with xpath "{xpath}"')
def set_key_to_xpath_attr(context, key, attr, xpath):
    assert context.persona is not None, "no persona is setup"
    try:
        el = context.browser.find_by_xpath(xpath)
    except ElementDoesNotExist:
        assert False, f'Element with xpath "{xpath}"not found'

    context.persona[key] = el.first[attr] or ""
