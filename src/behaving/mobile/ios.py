import time
import os
import xml.dom.minidom

from appium import webdriver
from splinter.driver.webdriver import BaseWebDriver
from splinter.element_list import ElementList


class IOSWebDriver(BaseWebDriver):

    driver_name = "ios"

    def __init__(self,
                 app_path,
                 appium_url='http://127.0.0.1:4723/wd/hub',
                 wait_time=2,
                 **kwargs):

        self.driver = webdriver.Remote(
            command_executor=appium_url,
            desired_capabilities={
                'app': os.path.expanduser(app_path),
                'platformName': 'iOS',
                'platformVersion': '11.2',
                'deviceName': 'iPhone 6',
                'automationName': 'XCUITest'
            }
        )
        super(IOSWebDriver, self).__init__(wait_time)



    def page_source(self):
        x = xml.dom.minidom.parseString(self.driver.page_source)
        return x.toprettyxml()

    def find_by(self, finder, selector):
        elements = None
        end_time = time.time() + self.wait_time

        while time.time() < end_time:
            try:
                elements = finder(selector)
                if not isinstance(elements, list):
                    elements = [elements]
            except NoSuchElementException:
                pass

            if elements:
                return ElementList(elements)
        return ElementList([])

    def find_by_accessibility_id(self, id):
        return self.find_by(self.driver.find_elements_by_accessibility_id, id)

    def is_text_present(self, text, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            text_elements = self.driver.find_elements_by_class_name('XCUIElementTypeStaticText')
            for el in text_elements:
                try:
                    el.text.index(text)
                    return True
                except ValueError:
                    continue
        return False

    def fill(self, name, value):
        field = self.find_by_accessibility_id(name).first
        assert field, u'No elements found with accessibility id %s' % name
        field.set_value(value)
