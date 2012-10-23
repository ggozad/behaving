import time
from behave import when, then


@then(u'I should see "{text}"')
def should_see(context, text):
    assert context.browser.is_text_present(text)


@then(u'I should not see "{text}"')
def should_not_see(context, text):
    assert context.browser.is_text_not_present(text)


@then(u'I should see "{text}" within {timeout:d} seconds')
def should_see_within_timeout(context, text, timeout):
    assert context.browser.is_text_present(text, wait_time=timeout)


@then(u'I should not see "{text}" within {timeout:d} seconds')
def should_not_see_within_timeout(context, text, timeout):
    assert context.browser.is_text_not_present(text)


@then(u'I should see an element with id "{id}"')
def should_see_element_with_id(context, id):
    assert context.browser.is_element_present_by_id(id)


@then(u'I should not see an element with id "{id}"')
def should_not_see_element_with_id(context, id):
    assert context.browser.is_element_not_present_by_id(id)


@then(u'I should see an element with id "{id}" within {timeout:d} seconds')
def should_see_element_with_id_within_timeout(context, id, timeout):
    assert context.browser.is_element_present_by_id(id, wait_time=timeout)


@then(u'I should not see an element with id "{id}" within {timeout:d} seconds')
def should_not_see_element_with_id_within_timeout(context, id, timeout):
    assert context.browser.is_element_not_present_by_id(id, wait_time=timeout)


@then(u'I should see an element with the css selector "{css}"')
def should_see_element_with_css(context, css):
    assert context.browser.is_element_present_by_css(css)


@then(u'I should not see an element with the css selector "{css}"')
def should_not_see_element_with_css(context, css):
    assert not context.browser.is_element_present_by_css(css)


@then(u'I should see an element with the css selector "{css}" within {timeout:d} seconds')
def should_see_element_with_css_within_timeout(context, css, timeout):
    assert context.browser.is_element_present_by_css(css, wait_time=timeout)


@then(u'I should not see an element with the css selector "{css}" within {timeout:d} seconds')
def should_not_see_element_with_css_within_timeout(context, css, timeout):
    assert not context.browser.is_element_present_by_css(css, wait_time=timeout)


@when(u'I wait for {timeout:d} seconds')
def wait_for_timeout(context, timeout):
    time.sleep(timeout)
