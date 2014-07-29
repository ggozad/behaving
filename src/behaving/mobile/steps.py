import base64
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


@step('I pull the file "{load_path}" from the app and set it to "{key}"')
def pull_file(context, load_path, key):
    try:
        b64 = context.device.pull_file(load_path)
        context.persona[key] = base64.b64decode(b64)
    except WebDriverException, e:
        assert False, e.msg


@step('I pull the file "{remote_path}" from the app and save it to "{local_path}"')
def pull_file(context, remote_path, local_path):
    try:
        b64 = context.device.pull_file(remote_path)
        with open(local_path, 'w') as f:
            f.write(base64.b64decode(b64))
            
    except WebDriverException, e:
        assert False, e.msg

@step('I push the file "{load_path}" to the device at "{save_path}"')
def push_file(context, load_path, save_path):
    full_path = os.path.join(context.device_data_path, load_path)
    with open(full_path, 'r') as f:
        data = f.read()
    data = base64.b64encode(data)
    try:
        context.device.push_file(save_path, data)
    except WebDriverException, e:
        assert False, e.msg


@step('I switch to the "{context_name}" context')
def switch_to_webview_context(context, context_name):
    try:
        context.device.switch_to.context(context_name)
    except WebDriverException, e:
        assert False, e.msg
