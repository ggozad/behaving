import os
from appium import webdriver
from behave import step


@step('an iOS simulator running "{name}"')
def given_an_ios_simulator(context, name):

    app_path = os.path.join(context.app_dir, name)
    context.mobile = webdriver.Remote(
        command_executor=context.webdriver_url,
        desired_capabilities={
            'app': app_path,
            'platformName': 'iOS',
            'platformVersion': '7.1',
            'deviceName': 'iPhone Simulator'
        })
