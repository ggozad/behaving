import os
import time

from . import setup, teardown


def before_all(context):
    setup(context)

    # Disable logging, selenium tends to be pretty verbose
    context.config.log_capture = False


def before_feature(context, feature):
    if "headless" in feature.tags:
        context.headless = True


def after_feature(context, feature):
    if "headless" in feature.tags:
        context.headless = False


def before_scenario(context, scenario):
    if "headless" in scenario.tags:
        context.headless = True
    if "noheadless" in scenario.tags:
        context.headless = False
    setup(context)


def after_scenario(context, scenario):
    if "headless" in scenario.tags:
        context.headless = False

    if (
        scenario.status == "failed"
        and context.screenshots_dir
        and hasattr(context, "browser")
    ):

        filename = (
            scenario.feature.name
            + u"-"
            + scenario.name
            + u"-"
            + time.strftime("%Y-%m-%d-%H%M%S", time.gmtime(time.time()))
        )
        filename = os.path.join(context.screenshots_dir, filename)
        try:
            context.browser.screenshot(filename)
        except Exception:
            pass
    teardown(context)


def after_all(context):
    teardown(context)
