from behave import step
from splinter.exceptions import ElementDoesNotExist

from behaving.personas.persona import persona_vars
from behaving.mobile.ios import IOSWebDriver
from behaving.mobile.android import AndroidWebDriver


@step(u'I should see an element with accessibility id "{id}"')
def see_accessibility_id(context, id):
    assert context.browser.find_by_accessibility_id(id), u"Element not found"


@step(u'I should see an element with iOS class chain "{chain}"')
def see_ios_class_chain(context, chain):
    assert context.browser.find_by_ios_class_chain(chain), u"Element not found"


@step(u'I press the element with iOS class chain "{chain}"')
def press_ios_class_chain(context, chain):
    assert isinstance(
        context.browser, IOSWebDriver
    ), "iOS class chain only available on iOS devices"
    el = context.browser.find_by_ios_class_chain(chain)
    assert el, u"Element not found"
    el.first.click()


@step(u"I press the element with android UiSelector '{selector}'")
def press_android_ui_selector(context, selector):
    assert isinstance(
        context.browser, AndroidWebDriver
    ), "Android UISelector only available on Android devices"
    el = context.browser.driver.find_element_by_android_uiautomator(selector)
    assert el, u"Element not found"
    el.click()


@step(u"I tap at {x:d} {y:d}")
def tap_at_coords(context, x, y):
    context.browser.driver.tap([(x, y)])


@step(u'I set "{key}" to the value of the element with iOS class chain "{chain}"')
@persona_vars
def set_variable(context, key, chain):
    assert isinstance(
        context.browser, IOSWebDriver
    ), "iOS class chain only available on iOS devices"
    assert context.persona is not None, u"no persona is setup"
    try:
        context.persona[key] = context.browser.find_by_ios_class_chain(
            chain
        ).first.get_attribute("value")
    except ElementDoesNotExist:
        assert False, u"Element not found"
