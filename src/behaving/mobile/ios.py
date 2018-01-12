import time
import os
import xml.dom.minidom

from appium import webdriver
from splinter.driver.webdriver import BaseWebDriver


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
        field = self.driver.find_elements_by_accessibility_id(name)
        assert field, u'No elements found with accessibility id %s' % name
        field = field[0]
        field.set_value(value)
