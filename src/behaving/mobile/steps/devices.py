import os

from behave import step
from ..ios import IOSWebDriver

@step(u'an iOS simulator running "{app_path}"')
def given_an_ios_app(context, app_path):
    app_path = os.path.join(context.mobile_app_dir, app_path)
    assert os.path.isdir(app_path), u'iOS app not found'
    app_path = os.path.abspath(app_path)
    context.ios_app = app_path
    context.browser = IOSWebDriver(app_path)
