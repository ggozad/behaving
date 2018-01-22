from behave import step


@step(u'I should see an element with accessibility id "{id}"')
def see_accessibility_id(context, id):
    assert context.browser.find_by_accessibility_id(id)


@step(u'I press the element with iOS class chain "{chain}"')
def press_class_chain(context, chain):
    el = context.browser.find_by_ios_class_chain(chain)
    assert el, u'Element not found'
    el.first.click()
