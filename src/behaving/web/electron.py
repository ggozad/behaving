from selenium.webdriver import Chrome
from splinter.browser import _DRIVERS
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement
from splinter.driver.webdriver.cookie_manager import CookieManager


class ElectronWebDriver(BaseWebDriver):

    driver_name = "Electron"

    def __init__(self, wait_time=2, fullscreen=False, binary=""):

        dc = {}
        dc["browserName"] = "electron"
        dc["chromeOptions"] = {
            "binary": binary,
        }
        self.driver = Chrome(desired_capabilities=dc)
        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(ElectronWebDriver, self).__init__(wait_time)


_DRIVERS["electron"] = ElectronWebDriver
