import mimetypes

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from splinter.driver.webdriver import (
    BaseWebDriver, WebDriverElement as WebDriverElement)
from splinter.driver.webdriver.cookie_manager import CookieManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

_DOWNLOAD_PATH = '/tmp'
_ALL_MIME_TYPES = ','.join(mimetypes.types_map.values())


class WebDriver(BaseWebDriver):

    driver_name = "Firefox"

    def __init__(self, profile=None, extensions=None, user_agent=None,
                 profile_preferences=None, fullscreen=False, wait_time=2):

        firefox_profile = FirefoxProfile(profile)
        firefox_profile.set_preference('extensions.logging.enabled', False)
        firefox_profile.set_preference('network.dns.disableIPv6', False)

        firefox_profile.set_preference("browser.download.folderList", 2)
        firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
        firefox_profile.set_preference("browser.download.dir", _DOWNLOAD_PATH)
        firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", _ALL_MIME_TYPES)
        # firefox_profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        # firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)

        if user_agent is not None:
            firefox_profile.set_preference(
                'general.useragent.override', user_agent)

        if profile_preferences:
            for key, value in profile_preferences.items():
                firefox_profile.set_preference(key, value)

        if extensions:
            for extension in extensions:
                firefox_profile.add_extension(extension)

        self.driver = Firefox(firefox_profile)

        if fullscreen:
            ActionChains(self.driver).send_keys(Keys.F11).perform()

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__(wait_time)

from splinter.browser import _DRIVERS
_DRIVERS['firefox'] = WebDriver
