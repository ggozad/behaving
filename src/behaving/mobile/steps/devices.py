import os

from behave import step
from ..ios import IOSWebDriver


@step(u'an iOS simulator running "{app_path}"')
def given_an_ios_app(context, app_path):
    # If the simulator exists
    app_path = os.path.join(context.mobile_app_dir, app_path)
    assert os.path.isdir(app_path), u'iOS app not found'
    app_path = os.path.abspath(app_path)
    if app_path in context.mobile_app_cache:
        context.browser = context.mobile_app_cache[app_path]
        context.browser.driver.launch_app()
    else:
        context.ios_app = app_path
        context.browser = IOSWebDriver(app_path)
        context.mobile_app_cache[app_path] = context.browser
