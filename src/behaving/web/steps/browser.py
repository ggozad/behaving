import os
import time
import logging

from behave import given, when
from selenium.common.exceptions import WebDriverException
from splinter import browser
from splinter.browser import Browser
from splinter.config import Config
from splinter.driver.webdriver.chrome import WebDriver as ChromeWebDriver

from behaving.web import DOWNLOAD_PATH, ALL_MIME_TYPES

logger = logging.getLogger(__name__)

browser._DRIVERS.update({
    "electron": ChromeWebDriver,
})


@given("{brand} as the default browser")
def given_some_browser(context, brand):
    brand = brand.lower()
    context.default_browser = brand


@given("a browser")
def given_a_browser(context):
    named_browser(context, "")


def get_default_selenium_options(driver_name, args):
    browser_name = driver_name.upper()
    # Handle case where user specifies IE with a space in it
    if browser_name == "INTERNET EXPLORER":
        browser_name = "INTERNETEXPLORER"

    # Collect correct Options class for Selenium based on browser.
    if browser_name in ("CHROME", "ELECTRON", "REMOTE"):
        from selenium.webdriver.chrome.options import Options
        options = Options()

        options.add_argument("--use-fake-device-for-media-stream")
        options.add_argument("--use-fake-ui-for-media-stream")

        prefs = {
            "profile.default_content_settings.popups": 0,
            "download.default_directory": DOWNLOAD_PATH,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "safebrowsing.disable_download_protection": True,
        }

        options.add_experimental_option("prefs", prefs)

    elif browser_name == "EDGE":
        from selenium.webdriver.edge.options import Options
        if "options" in args and isinstance(args["options"], Options):
            options = args["options"]
        else:
            options = Options()

    elif browser_name == "FIREFOX":
        from selenium.webdriver.firefox.options import Options
        from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
        if "options" in args and isinstance(args["options"], Options):
            options = args["options"]
        else:
            options = Options()

        profile = args.pop("profile", None)
        firefox_profile = FirefoxProfile(profile)
        firefox_profile.set_preference("extensions.logging.enabled", False)
        firefox_profile.set_preference("network.dns.disableIPv6", False)

        firefox_profile.set_preference("browser.download.folderList", 2)
        firefox_profile.set_preference(
            "browser.download.manager.showWhenStarting", False
        )
        firefox_profile.set_preference("browser.download.dir", DOWNLOAD_PATH)
        firefox_profile.set_preference(
            "browser.helperApps.neverAsk.saveToDisk", ALL_MIME_TYPES
        )
        firefox_profile.set_preference("permissions.default.microphone", 1)
        firefox_profile.set_preference("permissions.default.camera", 1)
        # firefox_profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        # firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)

        if args("profile_preferences"):
            for key, value in args("profile_preferences").items():
                firefox_profile.set_preference(key, value)
            args.pop("profile_preferences", None)

    elif browser_name == "SAFARI":
        from selenium.webdriver.safari.options import Options
        if "options" in args and isinstance(args["options"], Options):
            options = args["options"]
        else:
            options = Options()

    elif browser_name == "EDGE":
        from selenium.webdriver.edge.options import Options
        if "options" in args and isinstance(args["options"], Options):
            options = args["options"]
        else:
            options = Options()
    elif browser_name == "INTERNETEXPLORER":
        from selenium.webdriver.ie.options import Options
        if "options" in args and isinstance(args["options"], Options):
            options = args["options"]
        else:
            options = Options()

    else:
        raise ValueError(f"Unsupported browser {browser_name}")

    return options


@given('browser "{name}"')
def named_browser(context, name):
    if getattr(context, "headless", None):
        context.browser_args["headless"] = True
    else:
        context.browser_args["headless"] = False

    if name not in context.browsers:
        args = context.browser_args.copy()
        if context.accept_ssl_certs:
            if "arguments" not in args:
                args["arguments"] = []
            args["arguments"].append("--ignore-certificate-errors")

        if context.remote_webdriver_url:
            driver_name = "remote"
            del args["headless"]
            if context.default_browser:
                args["browser"] = context.default_browser
                args["command_executor"] = context.remote_webdriver_url
        elif context.default_browser:
            driver_name = context.default_browser
        else:
            driver_name = "firefox"

        if context.default_browser == "electron":
            assert context.electron_app, "You need to set the electron app path"
            args["binary"] = context.electron_app
        browser_attempts = 0
        while browser_attempts < context.max_browser_attempts:
            try:
                # Generate Splinter Config
                config = Config()
                if getattr(args, 'extensions', None) and isinstance(args['extensions'], list):
                    config.extensions = args("extensions")
                args.pop('extensions', None)
                config.fullscreen = getattr(args, 'fullscreen', False)
                args.pop('fullscreen', None)
                config.headless = getattr(args, "headless", False)
                args.pop('headless', None)
                config.incognito = getattr(args, "incognito", False)
                args.pop('incognito', None)
                config.user_agent = getattr(args, 'user_agent', None)
                args.pop('user_agent', None)

                # Generate Selenium Options
                options = get_default_selenium_options(driver_name, args)
                args["options"] = options

                if "arguments" in args:
                    for arg in args["arguments"]:
                        options.add_argument(arg)
                    args.pop("arguments", None)

                if "capabilities" in args:
                    for key, value in args["capabilities"]:
                        options.set_capability(key, value)
                    args.pop("capabilities", None)

                if "desired_capabilities" in args:
                    # Legacy name
                    for key, value in args["desired_capabilities"].items():
                        options.set_capability(key, value)
                    args.pop("desired_capabilities", None)

                retry_count = getattr(args, 'retry_count', 3)
                context.browsers[name] = Browser(driver_name=driver_name,
                                                 retry_count=retry_count,
                                                 config=config,
                                                 **args)
                break
            except WebDriverException as e:
                browser_attempts += 1
                if (browser_attempts < context.max_browser_attempts):
                    raise e
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
    context.browser.cookies.delete_all()


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
