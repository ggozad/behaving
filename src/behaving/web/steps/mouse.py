from behave import when

from behaving.personas.persona import persona_vars


@when('I mouse over the element with xpath "{xpath}"')
@persona_vars
def mouse_over(context, xpath):
    element = context.browser.find_by_xpath(xpath)
    assert element, f"Element with xpath {xpath} not found"
    element.mouse_over()


@when('I mouse out of the element with xpath "{xpath}"')
def mouse_out(context, xpath):
    element = context.browser.find_by_xpath(xpath)
    assert element, f"Element with xpath {xpath} not found"
    element.mouse_out()
