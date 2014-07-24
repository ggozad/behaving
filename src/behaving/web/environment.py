import os
import time

from . import setup, teardown


def before_all(context):
    setup(context)

    # Disable logging, selenium tends to be pretty verbose
    context.config.log_capture = False


def before_feature(context, feature):
    pass


def before_scenario(context, scenario):
    setup(context)


def after_feature(context, feature):
    pass


def after_scenario(context, scenario):
    if scenario.status == 'failed' and \
       context.screenshots_dir and \
       hasattr(context, 'browser'):

        filename = scenario.feature.name + u'-' + \
            scenario.name + u'-' + \
            time.strftime("%Y-%m-%d-%H%M%S", time.gmtime(time.time()))
        filename = os.path.join(context.screenshots_dir, filename)
        try:
            context.browser.screenshot(filename)
        except:
            pass
    teardown(context)


def after_all(context):
    teardown(context)
