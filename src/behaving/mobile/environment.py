import os
import subprocess
from . import setup, teardown


def before_all(context):
    # Unlock the android emulator so that we can install and run an app
    android_home = os.environ.get('ANDROID_HOME')
    if android_home:
        try:
            subprocess.call([os.path.join(android_home, 'platform-tools', 'adb'), 'shell', 'input', 'keyevent', '82'])
        except OSError:
            pass


def before_feature(context, feature):
    pass


def before_scenario(context, scenario):
    setup(context)


def after_feature(context, feature):
    pass


def after_scenario(context, scenario):
    teardown(context)


def after_all(context):
    teardown(context)
