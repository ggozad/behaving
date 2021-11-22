# -*- coding: utf-8 -*-

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement
from splinter.driver.webdriver.cookie_manager import CookieManager
from splinter.browser import _DRIVERS

_DOWNLOAD_PATH = "/tmp"


class WebDriver(BaseWebDriver):

    driver_name = "Chrome"

    def __init__(
        self,
        user_agent=None,
        wait_time=2,
        fullscreen=False,
        options=None,
        headless=False,
        **kwargs
    ):

        options = Options() if options is None else options

        if user_agent is not None:
            options.add_argument("--user-agent=" + user_agent)

        options.add_argument("--use-fake-device-for-media-stream")
        options.add_argument("--use-fake-ui-for-media-stream")
        if fullscreen:
            options.add_argument("--kiosk")

        if headless:
            # noinspection PyDeprecation
            # windows: chrome version >= 60
            options.set_headless()

        prefs = {
            "download": {
                "default_directory": _DOWNLOAD_PATH,
                "directory_upgrade": True,
                "extensions_to_open": "",
            }
        }

        options.add_experimental_option("prefs", prefs)

        self.driver = Chrome(chrome_options=options, **kwargs)

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__(wait_time)


_DRIVERS["chrome"] = WebDriver
