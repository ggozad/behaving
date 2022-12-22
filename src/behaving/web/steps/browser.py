import os
import time

from behave import given, when
from selenium.common.exceptions import WebDriverException
from splinter.browser import Browser


@given("{brand} as the default browser")
def given_some_browser(context, brand):
    brand = brand.lower()
    context.default_browser = brand


@given("a browser")
def given_a_browser(context):
    if getattr(context, "headless", None):
        context.browser_args["headless"] = True
    else:
        context.browser_args["headless"] = False

    named_browser(context, "")


@given('browser "{name}"')
def named_browser(context, name):
    if getattr(context, "headless", None):
        context.browser_args["headless"] = True
    else:
        context.browser_args["headless"] = False

    if name not in context.browsers:
        args = context.browser_args.copy()
        if context.accept_ssl_certs:
            if "desired_capabilities" not in args:
                args["desired_capabilities"] = {}
            args["desired_capabilities"].update({"acceptInsecureCerts": True})
        if context.remote_webdriver_url:
            args["driver_name"] = "remote"
            del args["headless"]
            if context.default_browser:
                args["browser"] = context.default_browser
                args["command_executor"] = context.remote_webdriver_url
        elif context.default_browser:
            args["driver_name"] = context.default_browser
        if context.default_browser == "electron":
            assert context.electron_app, "You need to set the electron app path"
            args["binary"] = context.electron_app
        browser_attempts = 0
        while browser_attempts < context.max_browser_attempts:
            try:
                context.browsers[name] = Browser(**args)
                break
            except WebDriverException:
                browser_attempts += 1
        else:
            raise WebDriverException("Failed to initialize browser")
        if context.default_browser_size:
            context.browsers[name].driver.set_window_size(*context.default_browser_size)

    context.browser = context.browsers[name]


@given('the electron app "{app_path}"')
def given_an_electron_app(context, app_path):
    assert os.path.isfile(app_path), "Electron app not found"
    app_path = os.path.abspath(app_path)
    context.electron_app = app_path


@when('I close the browser "{name}"')
def close_browser(context, name):
    context.browsers[name].driver.close()
    del context.browsers[name]


@when("I reload")
def reload(context):
    context.browser.reload()


@when("I go back")
def go_back(context):

    context.browser.back()


@when("I go forward")
def go_forward(context):
    context.browser.forward()


@when('I set the cookie "{key}" to "{value}"')
def set_cookie(context, key, value):
    context.browser.cookies.add({key: value})


@when('I delete the cookie "{key}"')
def delete_cookie(context, key):
    context.browser.cookies.delete(key)


@when("I delete all cookies")
def delete_all_cookies(context):
    context.browser.cookies.delete()


@when("I clear the localStorage")
def clear_local_storage(context):
    context.browser.execute_script("localStorage.clear();")


@when("I clear the sessionStorage")
def clear_session_storage(context):
    context.browser.execute_script("sessionStorage.clear();")


@when("I clear the browser storage")
def clear_browser_storage(context):
    context.browser.execute_script("localStorage.clear();sessionStorage.clear();")


@when("I resize the browser to {width}x{height}")
def resize_browser(context, width, height):
    context.browser.driver.set_window_size(int(width), int(height))


@when("I resize the viewport to {width}x{height}")
def resize_viewport(context, width, height):
    width = int(width)
    height = int(height)

    b_size = context.browser.driver.get_window_size()
    b_width = b_size["width"]
    b_height = b_size["height"]
    v_width = context.browser.evaluate_script("document.documentElement.clientWidth")
    v_height = context.browser.evaluate_script("document.documentElement.clientHeight")

    context.browser.driver.set_window_size(
        b_width + width - v_width, b_height + height - v_height
    )


@when("I maximize the browser's window")
def maximize_window(context):
    context.browser.driver.maximize_window()


@when("I take a screenshot")
def take_screenshot(context):

    assert context.screenshots_dir != "", "no screenshots_dir specified"

    filename = (
        context.scenario.feature.name
        + "-"
        + context.scenario.name
        + "-"
        + time.strftime("%Y-%m-%d-%H%M%S", time.gmtime(time.time()))
    )
    filename = os.path.join(context.screenshots_dir, filename)
    context.browser.screenshot(filename)
