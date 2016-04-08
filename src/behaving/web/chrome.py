# -*- coding: utf-8 -*-

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement
from splinter.driver.webdriver.cookie_manager import CookieManager

_DOWNLOAD_PATH = '/tmp'


class WebDriver(BaseWebDriver):

    driver_name = "Chrome"

    def __init__(self, user_agent=None, wait_time=2, fullscreen=False,
                 **kwargs):

        options = Options()

        if user_agent is not None:
            options.add_argument("--user-agent=" + user_agent)

        if fullscreen:
            options.add_argument('--kiosk')

        prefs = {"download": {
            "default_directory": _DOWNLOAD_PATH,
            "directory_upgrade": True,
            "extensions_to_open": ""
        }}

        options.add_experimental_option("prefs", prefs)

        self.driver = Chrome(chrome_options=options, **kwargs)

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__(wait_time)


from splinter.browser import _DRIVERS
_DRIVERS['chrome'] = WebDriver
