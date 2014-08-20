import os
import time

from behave import step
from splinter.browser import Browser
from selenium.common.exceptions import WebDriverException

from behaving.mobile.multiplatform import multiplatform


@step(u'a browser')
def given_a_browser(context):
    named_browser(context, '')


@step(u'browser "{name}"')
def named_browser(context, name):
    single_browser = hasattr(context, 'single_browser')
    if single_browser and hasattr(context, 'browser') and context.browser == name:
        #  don't start up multiple browsers
        return
    if name not in context.browsers:
        args = context.browser_args.copy()
        if context.remote_webdriver:
            args['driver_name'] = 'remote'
            if context.default_browser:
                args['browser'] = context.default_browser
        elif context.default_browser:
            args['driver_name'] = context.default_browser
        browser_attempts = 0
        while browser_attempts < context.max_browser_attempts:
            try:
                context.browsers[name] = Browser(**args)
                break
            except WebDriverException:
                browser_attempts += 1
        else:
            raise WebDriverException("Failed to initialize browser")
    context.browser = context.browsers[name]
    context.browser.switch_to_window(context.browser.windows[0])
    if single_browser:
        context.is_connected = True
    if context.default_browser_size:
        context.browser.driver.set_window_size(*context.default_browser_size)


@step(u'{brand} as the default browser')
def given_some_browser(context, brand):
    brand = brand.lower()
    context.default_browser = brand


@step(u'I reload')
def reload(context):
    context.browser.reload()


@step(u'I go back')
@multiplatform
def go_back(context):
    def browser(context):
        context.browser.back()

    def mobile(context):
        context.device.back()


@step(u'I go forward')
def go_forward(context):
    context.browser.forward()


@step(u'I set the cookie "{key}" to "{value}"')
def set_cookie(context, key, value):
    context.browser.cookies.add({key: value})


@step(u'I delete the cookie "{key}"')
def delete_cookie(context, key):
    context.browser.cookies.delete(key)


@step(u'I delete all cookies')
def delete_all_cookies(context):
    context.browser.cookies.delete()


@step(u'I resize the browser to {width}x{height}')
def resize_browser(context, width, height):
    context.browser.driver.set_window_size(int(width), int(height))


@step(u'I resize the viewport to {width}x{height}')
def resize_viewport(context, width, height):
    width = int(width)
    height = int(height)

    b_size = context.browser.driver.get_window_size()
    b_width = b_size['width']
    b_height = b_size['height']
    v_width = context.browser.evaluate_script("document.documentElement.clientWidth")
    v_height = context.browser.evaluate_script("document.documentElement.clientHeight")

    context.browser.driver.set_window_size(
        b_width + width - v_width,
        b_height + height - v_height)


@step(u'I take a screenshot')
@multiplatform
def take_screenshot(context):

    def _get_filename():
        assert context.screenshots_dir != '', u'no screenshots_dir specified'

        filename = context.scenario.feature.name + u'-' + \
            context.scenario.name + u'-' + \
            time.strftime("%Y-%m-%d-%H%M%S", time.gmtime(time.time()))
        filename = os.path.join(context.screenshots_dir, filename)
        return filename

    def browser(context):
        filename = _get_filename()
        context.browser.screenshot(filename)

    def mobile(context):
        filename = _get_filename() + '.png'
        assert context.device.save_screenshot(filename), u'Could not save screenshot'
