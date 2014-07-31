import base64
import os
import logging
from urllib2 import URLError
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import WebDriverException
from behave import step


@step('an iOS simulator running "{name}"')
def given_an_ios_simulator_running_app(context, name):
    given_an_ios_simulator_running_app_with_reset(context, name, True)

@step('a dirty iOS simulator running "{name}"')
def given_an_ios_simulator_running_app(context, name):
    given_an_ios_simulator_running_app_with_reset(context, name, False)

def given_an_ios_simulator_running_app_with_reset(context, name, reset):
    if reset:
        logging.debug("Starting a clean iOS simulator with %s" % name)
    else:
        logging.debug("Starting a dirty iOS simulator with %s" % name)
    app_path = os.path.join(context.app_dir, name)
    context.ios_app_name = name

    try:
        context.device = webdriver.Remote(
            command_executor=context.webdriver_url,
            desired_capabilities=dict(context.ios_caps, app=app_path, noReset=not reset)
        )
    except URLError:
        assert False, 'Appium is not running on the specified webdriver_url'

@step('I restart the iOS simulator')
def restart_the_ios_simulator(context):
    if hasattr(context, 'device'):
        context.device.quit()
    given_an_ios_simulator_running_app_with_reset(context, context.ios_app_name, False)

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
    el = context.device.find_element_by_name(name)
    action = TouchAction(context.device)
    action.press(el)
    for pair in coords:
        action.move_to(x=pair[0], y=pair[1])
    action.release()
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


@step('I reset the app')
def close_app(context):
    try:
        context.device.reset()
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
    logging.debug("pulling file %s to %s" % (remote_path, local_path))
    try:
        b64 = context.device.pull_file(remote_path)
        with open(local_path, 'w') as f:
            f.write(base64.b64decode(b64))
            
    except WebDriverException, e:
        logging.debug("failed to pull file")
        assert False, e.msg

    logging.debug("done")
@step('I push the file "{load_path}" to the device at "{save_path}"')
def push_file(context, load_path, save_path):
    if not load_path.startswith("/"):
        load_path = os.path.join(context.device_data_path, load_path)

    logging.debug("pushing file %s to %s" % (load_path, save_path))
    with open(load_path, 'r') as f:
        data = f.read()
    data = base64.b64encode(data)
    try:
        context.device.push_file(save_path, data)
    except WebDriverException, e:
        assert False, e.msg


@step('I switch to the "{context_name}" context')
def switch_to_webview_context(context, context_name):
    error = None
    try:
        for c in context.device.contexts:
            if c.startswith(context_name):
                context.device.switch_to.context(c)
                return
    except WebDriverException, e:
        error = e.msg

    if error != None:
        assert False, "%s. Available contexts: %s" % (error, context.device.contexts)
