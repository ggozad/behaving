from behave import when
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


@when(u'I switch to frame with css "{css}"')
def switch_to_frame(context, css):
    driver = context.browser.driver
    try:
        frame = driver.find_element(By.CSS_SELECTOR, css)
    except NoSuchElementException:
        assert False, f'Frame with css selector "{css}" not found'
    driver.switch_to.frame(frame)


@when(u"I switch back to the main page")
def switch_to_main_page(context):
    context.browser.driver.switch_to.default_content()
