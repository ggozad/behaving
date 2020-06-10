import time
import os
import xml.dom.minidom

from appium import webdriver
from splinter.driver.webdriver import BaseWebDriver
from splinter.element_list import ElementList
from selenium.common.exceptions import WebDriverException
from splinter.browser import _DRIVERS


class IOSWebDriver(BaseWebDriver):

    driver_name = "ios"

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
            "platformName": "iOS",
            "platformVersion": "13.2",
            "deviceName": "iPhone SE",
            "noReset": True,
            "newCommandTimeout": 50000,
        }
        desired_capabilities.update(caps)
        self.driver = webdriver.Remote(
            command_executor=appium_url, desired_capabilities=desired_capabilities
        )
        super(IOSWebDriver, self).__init__(wait_time)

    def udid(self):
        return self.driver.capabilities.get("udid")

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

    def find_by_xpath(self, xpath):
        return self.find_by(self.driver.find_element_by_xpath, xpath)

    def find_by_accessibility_id(self, id):
        return self.find_by(self.driver.find_elements_by_accessibility_id, id)

    def find_by_ios_class_chain(self, query):
        return self.find_by(self.driver.find_element_by_ios_class_chain, query)

    def _is_text_present(self, text):
        text_elements = self.driver.find_elements_by_class_name(
            "XCUIElementTypeStaticText"
        )
        for el in text_elements:
            try:
                el.text.index(text)
                if el.get_attribute("visible") == "true":
                    return True
            except (
                ValueError,
                AttributeError,
            ):
                continue
        try:
            self.driver.find_element_by_ios_class_chain(
                '**/XCUIElementTypeOther[`name CONTAINS "%s" AND visible==true`]' % text
            )
            return True
        except WebDriverException:
            return False
        return False

    def is_text_present(self, text, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            if self._is_text_present(text):
                return True
        return False

    def is_text_not_present(self, text, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            if not self._is_text_present(text):
                return True
        return False

    def fill(self, name, value):
        field = self.find_by_accessibility_id(name)
        if not field:
            field = self.find_by_ios_class_chain(
                '**/XCUIElementTypeTextView[`name CONTAINS "%s"`]' % name
            )

        assert field, u"No elements found with accessibility id or name %s" % name
        try:
            field.first.set_value(value)
        except WebDriverException:
            # For some reason Appium fails on first try
            # If you first don't succeed, try again is what they say
            field.first.set_value(value)


_DRIVERS["ios"] = IOSWebDriver
