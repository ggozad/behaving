from behave import step
from splinter.exceptions import ElementDoesNotExist
from appium.webdriver.common.touch_action import TouchAction

from behaving.personas.persona import persona_vars
from behaving.mobile.ios import IOSWebDriver
from behaving.mobile.android import AndroidWebDriver


@step(u'I should see an element with accessibility id "{id}"')
def see_accessibility_id(context, id):
    el = context.browser.find_by_accessibility_id(id)
    assert el, u"Element not found"
    assert el.is_displayed(), u"Element not in view"


@step(u'I should not see an element with accessibility id "{id}"')
def not_see_accessibility_id(context, id):
    el = context.browser.find_by_accessibility_id(id)
    assert el is None or el.is_displayed() == False, u"Element found"


@step(u'I should see an element with iOS class chain "{chain}"')
def see_ios_class_chain(context, chain):
    el = context.browser.find_by_ios_class_chain(chain)
    assert el, u"Element not found"
    assert el.is_displayed(), u"Element not in view"


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


@step(u'I scroll the element with accessibility id "{id}" by {x:d} {y:d}')
def scroll_element(context, id, x, y):
    el = context.browser.find_by_accessibility_id(id)
    assert el, u"Element not found"
    location = el.location
    actions = TouchAction(context.browser.driver)
    actions.tap(x=location["x"], y=location["y"]).wait(100).move_to(
        x=location["x"] + x, y=location["y"] + y
    ).wait(100).perform()

