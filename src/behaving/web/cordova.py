from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement
from splinter.driver.webdriver.cookie_manager import CookieManager


class CordovaWebDriver(BaseWebDriver):

    driver_name = "Cordova"

    def __init__(self, user_agent=None,
                 wait_time=2,
                 fullscreen=False,
                 persistent_session=False,
                 **kwargs):
        options = Options()

        if user_agent is not None:
            options.add_argument("--user-agent=" + user_agent)

        if fullscreen:
            options.add_argument('--kiosk')

        options.add_argument('-F')
        options.add_argument('--args')
        options.add_argument('--disable-web-security')
        if persistent_session:
            options.add_argument('--user-data-dir=/tmp/temp_chrome_user_data_dir_for_cordova_browser')
        else:
            options.add_argument('--incognito')

        dc = DesiredCapabilities.CHROME
        dc['loggingPrefs'] = {'browser': 'ALL'}

        self.driver = Chrome(chrome_options=options, desired_capabilities=dc, **kwargs)
        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(CordovaWebDriver, self).__init__(wait_time)

from splinter.browser import _DRIVERS
_DRIVERS['cordova'] = CordovaWebDriver
