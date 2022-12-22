import mimetypes

from selenium.webdriver import DesiredCapabilities, Firefox
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from splinter.browser import _DRIVERS
from splinter.driver.webdriver import BaseWebDriver
from splinter.driver.webdriver import WebDriverElement as WebDriverElement
from splinter.driver.webdriver.cookie_manager import CookieManager

_DOWNLOAD_PATH = "/tmp"
_ALL_MIME_TYPES = ",".join(mimetypes.types_map.values())


class WebDriver(BaseWebDriver):

    driver_name = "Firefox"

    def __init__(
        self,
        profile=None,
        extensions=None,
        user_agent=None,
        profile_preferences=None,
        fullscreen=False,
        options=None,
        headless=False,
        wait_time=2,
        desired_capabilities=None,
    ):

        firefox_profile = FirefoxProfile(profile)
        firefox_profile.set_preference("extensions.logging.enabled", False)
        firefox_profile.set_preference("network.dns.disableIPv6", False)

        firefox_profile.set_preference("browser.download.folderList", 2)
        firefox_profile.set_preference(
            "browser.download.manager.showWhenStarting", False
        )
        firefox_profile.set_preference("browser.download.dir", _DOWNLOAD_PATH)
        firefox_profile.set_preference(
            "browser.helperApps.neverAsk.saveToDisk", _ALL_MIME_TYPES
        )
        firefox_profile.set_preference("permissions.default.microphone", 1)
        firefox_profile.set_preference("permissions.default.camera", 1)
        # firefox_profile.set_preference("browser.helperApps.alwaysAsk.force", False)
        # firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)

        if user_agent is not None:
            firefox_profile.set_preference("general.useragent.override", user_agent)

        if profile_preferences:
            for key, value in profile_preferences.items():
                firefox_profile.set_preference(key, value)

        if extensions:
            for extension in extensions:
                firefox_profile.add_extension(extension)

        options = Options() if options is None else options

        if headless:
            # noinspection PyDeprecation
            options.set_headless()

        firefox_capabilities = DesiredCapabilities().FIREFOX.copy()
        firefox_capabilities["marionette"] = True
        if desired_capabilities:
            firefox_capabilities.update(desired_capabilities)

        self.driver = Firefox(
            firefox_profile, capabilities=firefox_capabilities, firefox_options=options
        )

        if fullscreen:
            ActionChains(self.driver).send_keys(Keys.F11).perform()

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__(wait_time)


_DRIVERS["firefox"] = WebDriver
