import os
import json
import subprocess

from behave import step


@step(u'the iOS app at "{app_path}"')
def given_an_ios_app(context, app_path):
    # If the simulator exists
    app_path = os.path.join(context.mobile_app_dir, app_path)
    assert os.path.isdir(app_path), u'iOS app not found'
    app_path = os.path.abspath(app_path)
    context.ios_app = app_path


@step(u'the android app at "{app_path}"')
def given_an_android_app(context, app_path):
    # If the simulator exists
    app_path = os.path.join(context.mobile_app_dir, app_path)
    assert os.path.isfile(app_path), u'Android app not found'
    app_path = os.path.abspath(app_path)
    context.android_app = app_path


@step(u'I set the iOS capabilities to "{caps}"')
def set_ios_capabilities(context, caps):
    context.ios_capabilities = json.loads(caps)


@step(u'I set the android capabilities to "{caps}"')
def set_android_capabilities(context, caps):
    context.android_capabilities = json.loads(caps)


@step(u'I launch the app')
def launch_app(context):
    context.browser.driver.launch_app()


@step(u'I close the app')
def close_app(context):
    context.browser.driver.close_app()


@step(u'I background the app')
def background_app(context):
    context.browser.driver.background_app(-1)


@step(u'I background the app for {timeout:d} seconds')
def background_app_with_timeout(context, timeout):
    context.browser.driver.background_app(timeout)


@step(u'I add "{path}" to the photo library')
def add_media(context, path):
    path = os.path.join(context.attachment_dir, path)
    subprocess.call(
        ['xcrun', 'simctl', 'addmedia',
         context.browser.udid(), path])


@step(u'I install the app')
def install_app(context):
    if context.browser.driver_name == 'ios':
        assert context.ios_app, u'No app specified'
        context.browser.driver.install_app(context.ios_app)
        return
    elif context.browser.driver_name == 'android':
        assert context.android_app, u'No app specified'
        context.browser.driver.install_app(context.android_app)
        return
    assert False, u'Not using a mobile device'