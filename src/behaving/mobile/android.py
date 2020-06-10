import time
import os
import xml.dom.minidom

from appium import webdriver
from splinter.driver.webdriver import BaseWebDriver
from splinter.element_list import ElementList
from selenium.common.exceptions import (
    WebDriverException,
    StaleElementReferenceException,
)
from splinter.browser import _DRIVERS


class AndroidWebDriver(BaseWebDriver):

    driver_name = "android"

    def __init__(
        self,
        app_path,
        appium_url="http://127.0.0.1:4723/wd/hub",
        wait_time=2,
        caps={},
        **kwargs
    ):

        self.app_path = app_path
        desired_capabilities = {
            "app": os.path.expanduser(app_path),
            "platformName": "Android",
            "automationName": "appium",
            "noReset": True,
            "newCommandTimeout": 50000,
        }
        desired_capabilities.update(caps)
        self.driver = webdriver.Remote(
            command_executor=appium_url, desired_capabilities=desired_capabilities
        )
        super(AndroidWebDriver, self).__init__(wait_time)

    def page_source(self):
        x = xml.dom.minidom.parseString(self.driver.page_source.encode("utf-8"))
        return x.toprettyxml()

    def find_by(self, finder, selector):
        elements = None
        end_time = time.time() + self.wait_time

        while time.time() < end_time:
            try:
                elements = finder(selector)
            except WebDriverException:
                elements = []
            if not isinstance(elements, list):
                elements = [elements]

            if elements:
                return ElementList(elements)
        return ElementList([])

    def find_by_accessibility_id(self, id):
        return self.find_by(self.driver.find_elements_by_accessibility_id, id)

    def find_by_xpath(self, xpath):
        return self.find_by(self.driver.find_element_by_xpath, xpath)

    def find_by_name(self, name):
        by_name = self.find_by(self.driver.find_element_by_name, name)
        if by_name:
            return by_name
        return self.find_by(self.driver.find_elements_by_accessibility_id, name)

    def _is_text_present(self, text):
        text_elements = self.driver.find_elements_by_class_name(
            "android.widget.TextView"
        )
        for el in text_elements:
            try:
                el.text.index(text)
                return True
            except (
                ValueError,
                AttributeError,
            ):
                continue
        return False

    def is_text_present(self, text, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            try:
                if self._is_text_present(text):
                    return True
            except StaleElementReferenceException:
                continue
        return False

    def is_text_not_present(self, text, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            try:
                if not self._is_text_present(text):
                    return True
            except StaleElementReferenceException:
                continue
        return False

    def fill(self, name, value):
        field = self.find_by_accessibility_id(name).first
        assert field, u"No elements found with accessibility id %s" % name
        field.set_value(value)


_DRIVERS["android"] = AndroidWebDriver
