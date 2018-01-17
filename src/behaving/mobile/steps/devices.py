import os

from behave import step


@step(u'the iOS app at "{app_path}"')
def given_an_ios_app(context, app_path):
    # If the simulator exists
    app_path = os.path.join(context.mobile_app_dir, app_path)
    assert os.path.isdir(app_path), u'iOS app not found'
    app_path = os.path.abspath(app_path)
    context.ios_app = app_path
