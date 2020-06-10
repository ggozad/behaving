from behave import step

from behaving.personas.persona import persona_vars


@step(u'I mouse over the element with xpath "{xpath}"')
@persona_vars
def mouse_over(context, xpath):
    element = context.browser.find_by_xpath(xpath)
    assert element, u"Element not found"
    element.mouse_over()


@step(u'I mouse out of the element with xpath "{xpath}"')
def mouse_out(context, xpath):
    element = context.browser.find_by_xpath(xpath)
    assert element, u"Element not found"
    element.mouse_out()
