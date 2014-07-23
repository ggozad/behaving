import os
from urllib2 import URLError

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from behave import step


@step('an iOS simulator running "{name}"')
def given_an_ios_simulator(context, name):

    app_path = os.path.join(context.app_dir, name)
    try:
        context.device = webdriver.Remote(
            command_executor=context.webdriver_url,
            desired_capabilities=dict(context.ios_caps, app=app_path)
        )
    except URLError:
        assert False, 'Appium is not running on the specified webdriver_url'


@step('an android simulator running "{name}"')
def given_an_android_simulator(context, name):

    app_path = os.path.join(context.app_dir, name)
    try:
        context.device = webdriver.Remote(
            command_executor=context.webdriver_url,
            desired_capabilities=dict(context.android_caps, app=app_path))
    except URLError:
        assert False, 'Appium is not running on the specified webdriver_url'


@step('I tap "{name}" and drag to "{coords}"')
def drag_name_to_coords(context, name, coords):
    coords = eval(coords)
    el = context.device.find_element_by_accessibility_id(name)
    action = TouchAction(context.device)
    action.press(el).move_to(x=0, y=0).move_to(x=100, y=0).move_to(x=0, y=100).release()
    action.perform()
