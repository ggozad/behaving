# Generic setup/teardown for compatibility with pytest et al.
import os
import atexit


def setup(context):

    if not hasattr(context, 'webdriver_url'):
        context.webdriver_url = 'http://127.0.0.1:4723/wd/hub'

    if hasattr(context, 'device_data_path'):
        if not os.path.isdir(context.device_data_path):
            os.mkdir(context.device_data_path)

    if not hasattr(context, 'android_caps'):
        context.android_caps = {
            'platformName': 'Android',
            'platformVersion': '4.4.2',
            'language': 'en',
            'deviceName': 'Android Emulator'
        }

    if not hasattr(context, 'ios_caps'):
        context.ios_caps = {
            'platformName': 'iOS',
            'platformVersion': '7.1',
            'language': 'en',
            'deviceName': 'iPhone'
        }

    # ensure we kill the appium server if the tests crash
    def cleanup():
        teardown(context)

    atexit.register(cleanup)


def teardown(context):
    if hasattr(context, 'device'):
        context.device.quit()
        del context.device
