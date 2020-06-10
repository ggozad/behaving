from behave import when


@when(u'I switch to frame with css "{css}"')
def switch_to_frame(context, css):
    driver = context.browser.driver
    frame = driver.find_element_by_css_selector(css)
    driver.switch_to_frame(frame)


@when(u"I switch back to the main page")
def switch_to_main_page(context):
    context.browser.driver.switch_to_default_content()
