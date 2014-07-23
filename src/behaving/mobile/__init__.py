# Generic setup/teardown for compatibility with pytest et al.
import logging

logger = logging.getLogger('behaving')


def setup(context):

    if not hasattr(context, 'webdriver_url'):
        context.webdriver_url = 'http://127.0.0.1:4723/wd/hub'
        logger.info('No default webdriver url is specified. Using %s' % context.webdriver_url)

    if not hasattr(context, 'android_caps'):
        context.android_caps = {
            'platformName': 'Android',
            'platformVersion': '4.4.2',
            'deviceName': 'Android Emulator'
        }

    if not hasattr(context, 'ios_caps'):
        context.ios_caps = {
            'platformName': 'iOS',
            'platformVersion': '7.1',
            'deviceName': 'iPhone Simulator'
        }


def teardown(context):
    pass
