# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement
from splinter.driver.webdriver.cookie_manager import CookieManager


class WebDriver(BaseWebDriver):

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

        self.driver = Chrome(chrome_options=options, **kwargs)
        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__(wait_time)


from splinter.browser import _DRIVERS
_DRIVERS['cordova'] = WebDriver
