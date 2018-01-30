import os
import json

from behave import step


@step(u'the iOS app at "{app_path}"')
def given_an_ios_app(context, app_path):
    # If the simulator exists
    app_path = os.path.join(context.mobile_app_dir, app_path)
    assert os.path.isdir(app_path), u'iOS app not found'
    app_path = os.path.abspath(app_path)
    context.ios_app = app_path


@step(u'I set the iOS capabilities to "{caps}"')
def set_ios_capabilities(context, caps):
    context.ios_capabilities = json.loads(caps)


@step(u'I launch the app')
def launch_app(context):
    context.browser.driver.launch_app()


@step(u'I close the app')
def close_app(context):
    context.browser.driver.close_app()
