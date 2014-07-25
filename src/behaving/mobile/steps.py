import os
from urllib2 import URLError

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import WebDriverException
from behave import step


@step('an iOS simulator running "{name}"')
def given_an_ios_simulator_running_app(context, name):

    app_path = os.path.join(context.app_dir, name)
    try:
        context.device = webdriver.Remote(
            command_executor=context.webdriver_url,
            desired_capabilities=dict(context.ios_caps, app=app_path)
        )
    except URLError:
        assert False, 'Appium is not running on the specified webdriver_url'


@step('an android simulator running "{name}"')
def given_an_android_simulator_running_app(context, name):

    app_path = os.path.join(context.app_dir, name)
    try:
        context.device = webdriver.Remote(
            command_executor=context.webdriver_url,
            desired_capabilities=dict(context.android_caps, app=app_path))
    except URLError:
        assert False, 'Appium is not running on the specified webdriver_url'


@step('I lock the device for {timeout:d} seconds')
def lock_device(context, timeout):
    context.device.lock(timeout)


@step('I tap "{name}" and drag to "{coords}"')
def drag_name_to_coords(context, name, coords):
    coords = eval(coords)
    el = context.device.find_element_by_accessibility_id(name)
    action = TouchAction(context.device)
    action.press(el).move_to(x=0, y=0).move_to(x=100, y=0).move_to(x=0, y=100).release()
    action.perform()


@step('I install the app "{name}"')
def install_application(context, name):
    # Does not work on iOS
    app_path = os.path.join(context.app_dir, name)
    try:
        context.device.install_app(app_path)
    except WebDriverException, e:
        assert False, e.msg


@step('I remove the app "{uid}"')
def remove_application(context, uid):
    # Does not work on iOS
    try:
        context.device.remove_app(uid)
    except WebDriverException, e:
        assert False, e.msg


@step('I launch the app')
def launch_app(context):
    try:
        context.device.launch_app()
    except WebDriverException, e:
        assert False, e.msg


@step('I close the app')
def close_app(context):
    try:
        context.device.close_app()
    except WebDriverException, e:
        assert False, e.msg


@step('the application "{uid}" is installed')
def application_is_installed(context, uid):
    assert context.device.is_app_installed(uid), 'Application %s is not installed' % uid


@step('I save the folder "{load_path}" from the app to "{save_path}"')
def save_folder(context, load_path, save_path):
    zipped = context.device.pull_folder(load_path)
    assert zipped


@step('I save the file "{load_path}" from the app to "{save_path}"')
def save_file(context, load_path, save_path):
    b64 = context.device.pull_file(load_path)
    assert b64
