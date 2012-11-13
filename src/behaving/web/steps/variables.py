from behave import when


@when('I set "{key}" to the text of "{name}"')
def set_key_to_el_text(context, key, name):
    assert context.persona is not None, u'no persona is setup'
    el = context.browser.find_by_id(name) or context.browser.find_by_name(name)
    assert el, u'Element not found'
    context.persona[key] = el.first.text
