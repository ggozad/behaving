import time
from behave import step

from behaving.personas.persona import persona_vars


@step(u'I wait for {timeout:d} seconds')
def wait_for_timeout(context, timeout):
    time.sleep(timeout)


@step(u'I show the element with id "{id}"')
def show_element_by_id(context, id):
    assert context.browser.find_by_id(id)
    context.browser.execute_script('document.getElementById("%s").style.display="inline";' % id)


@step(u'I hide the element with id "{id}"')
def hide_element_by_id(context, id):
    assert context.browser.find_by_id(id)
    context.browser.execute_script('document.getElementById("%s").style.display="none";' % id)


@step(u'I should see "{text}"')
def should_see(context, text):
    assert context.browser.is_text_present(text), u'Text not found'


@step(u'I should not see "{text}"')
def should_not_see(context, text):
    assert context.browser.is_text_not_present(text), u'Text was found'


@step(u'I should see "{text}" within {timeout:d} seconds')
def should_see_within_timeout(context, text, timeout):
    assert context.browser.is_text_present(text, wait_time=timeout), u'Text not found'


@step(u'I should not see "{text}" within {timeout:d} seconds')
def should_not_see_within_timeout(context, text, timeout):
    assert context.browser.is_text_not_present(text, wait_time=timeout), u'Text was found'


@step(u'I should see an element with id "{id}"')
def should_see_element_with_id(context, id):
    assert context.browser.is_element_present_by_id(id), u'Element not present'


@step(u'I should not see an element with id "{id}"')
def should_not_see_element_with_id(context, id):
    assert context.browser.is_element_not_present_by_id(id), u'Element is present'


@step(u'I should see an element with id "{id}" within {timeout:d} seconds')
def should_see_element_with_id_within_timeout(context, id, timeout):
    assert context.browser.is_element_present_by_id(id, wait_time=timeout), u'Element not present'


@step(u'I should not see an element with id "{id}" within {timeout:d} seconds')
def should_not_see_element_with_id_within_timeout(context, id, timeout):
    assert context.browser.is_element_not_present_by_id(id, wait_time=timeout), u'Element is present'


@step(u'I should see an element with the css selector "{css}"')
def should_see_element_with_css(context, css):
    assert context.browser.is_element_present_by_css(css), u'Element not present'


@step(u'I should not see an element with the css selector "{css}"')
def should_not_see_element_with_css(context, css):
    assert not context.browser.is_element_present_by_css(css), u'Element is present'


@step(u'I should see an element with the css selector "{css}" within {timeout:d} seconds')
def should_see_element_with_css_within_timeout(context, css, timeout):
    assert context.browser.is_element_present_by_css(css, wait_time=timeout), u'Element not present'


@step(u'I should not see an element with the css selector "{css}" within {timeout:d} seconds')
def should_not_see_element_with_css_within_timeout(context, css, timeout):
    assert not context.browser.is_element_present_by_css(css, wait_time=timeout), u'Element is present'


@step(u'I should see an element with xpath "{xpath}"')
@persona_vars
def should_see_element_with_xpath(context, xpath):
    print xpath
    assert context.browser.is_element_present_by_xpath(xpath), u'Element not present'


@step(u'I should not see an element with xpath "{xpath}"')
@persona_vars
def should_not_see_element_with_xpath(context, xpath):
    assert not context.browser.is_element_present_by_xpath(xpath), u'Element is present'


@step(u'I should see an element with xpath "{xpath}" within {timeout:d} seconds')
@persona_vars
def should_see_element_with_xpath_within_timeout(context, xpath, timeout):
    assert context.browser.is_element_present_by_xpath(xpath, wait_time=timeout), u'Element not present'


@step(u'I should not see an element with xpath "{xpath}" within {timeout:d} seconds')
@persona_vars
def should_not_see_element_with_xpath_within_timeout(context, xpath, timeout):
    assert not context.browser.is_element_present_by_xpath(xpath, wait_time=timeout), u'Element is present'
