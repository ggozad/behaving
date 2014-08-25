import base64
import os
from urllib2 import URLError
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from behave import step

from behaving.personas.persona import persona_vars
from behaving.mobile.multiplatform import multiplatform


def find_device_element_by_name_or_id(context, id):
    try:
        return context.device.find_element_by_id(id)
    except NoSuchElementException:
        try:
            return context.device.find_element_by_name(id)
        except NoSuchElementException:
            pass
    return None


def given_a_simulator_running_with_caps(context, caps):
    if hasattr(context, 'device'):
        context.device.quit()

    try:
        context.device = webdriver.Remote(
            command_executor=context.webdriver_url,
            desired_capabilities=caps
        )
    except URLError:
        assert False, 'Appium is not running on the specified webdriver_url'


@step('an iOS simulator running "{name}"')
def given_an_ios_simulator_running_app(context, name):
    app_path = os.path.join(context.app_dir, name)
    context.ios_app_name = name
    given_a_simulator_running_with_caps(context, dict(context.ios_caps, app=app_path, noReset=False))


@step('a dirty iOS simulator running "{name}"')
def given_a_dirty_ios_simulator_running_app(context, name):
    app_path = os.path.join(context.app_dir, name)
    context.ios_app_name = name
    given_a_simulator_running_with_caps(context, dict(context.ios_caps, app=app_path, noReset=True))


@step('I restart the iOS simulator')
def restart_the_ios_simulator(context):
    app_path = os.path.join(context.app_dir, context.ios_app_name)
    given_a_simulator_running_with_caps(context, dict(context.ios_caps, app=app_path, noReset=True))


@step('an android simulator running "{name}"')
def given_an_android_simulator_running_app(context, name):
    app_path = os.path.join(context.app_dir, name)
    context.android_app_name = name
    given_a_simulator_running_with_caps(context, dict(context.android_caps, app=app_path, noReset=False))


@step('a dirty android simulator running "{name}"')
def given_a_dirty_android_simulator_running_app(context, name):
    app_path = os.path.join(context.app_dir, name)
    context.android_app_name = name
    given_a_simulator_running_with_caps(context, dict(context.android_caps, app=app_path, noReset=True))


@step('I lock the device')
def lock_device(context):
    context.device.lock(5)


@step('I tap "{name}" and drag to "{coords}"')
@persona_vars
def drag_name_to_coords(context, name, coords):
    coords = eval(coords)
    el = find_device_element_by_name_or_id(context, name)
    assert el, u'Element not found'
    action = TouchAction(context.device)
    action.press(el)
    for pair in coords:
        action.move_to(x=pair[0], y=pair[1])
    action.release()
    action.perform()


@step('I slide "{name}" to {percent:d}%')
@persona_vars
@multiplatform
def slide_to_percent(context, name, percent):

    def ios(context, name, percent):
        el = find_device_element_by_name_or_id(context, name)
        assert el, u'Element not found'
        el.set_value(percent / 100.0)


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
def reset_app(context):
    try:
        context.device = context.device.reset()
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
def pull_save_file(context, remote_path, local_path):
    try:
        b64 = context.device.pull_file(remote_path)
        with open(local_path, 'w') as f:
            f.write(base64.b64decode(b64))

    except WebDriverException, e:
        assert False, e.msg


@step('I push the file "{load_path}" to the device at "{save_path}"')
def push_file(context, load_path, save_path):
    if not load_path.startswith("/"):
        load_path = os.path.join(context.device_data_path, load_path)

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

    if error is not None:
        assert False, "%s. Available contexts: %s" % (error, context.device.contexts)
