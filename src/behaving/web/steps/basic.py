import time
from behave import step
from selenium.common.exceptions import NoSuchElementException

from behaving.personas.persona import persona_vars
from behaving.mobile.multiplatform import multiplatform
from behaving.mobile.steps import find_device_element_by_name_or_id


# Accepts a lambda as first paramter, returns lambda result on success, or False on timeout
def _retry(func, timeout=0, delay=1):
    assert isinstance(func, type(lambda: None)), "Retry expects a lambda as the first argument"

    start = time.time()
    while True:
        try:
            res = func()
            if not res:
                time.sleep(delay)
            else:
                return res
        except:
            time.sleep(delay)

        if time.time() - start > timeout:
            return None


def texts_on_device(context, id=None):
    if context.device.name == 'Android':
        elems = context.device.find_elements_by_class_name('android.widget.TextView')
        return [e.text for e in elems]
    else:
        elems = context.device.find_elements_by_class_name('UIAStaticText')
        return [e.get_attribute("label") for e in elems]


def text_exists_on_device(context, text, id=None):
    # This should be replaced with something more sane
    # It also only works on iOS
    texts = texts_on_device(context, id)
    for t in texts:
        try:
            if text in t:
                return True
        except UnicodeEncodeError:
            pass

    return False


@step(u'I wait for {timeout:d} seconds')
@persona_vars
def wait_for_timeout(context, timeout):
    time.sleep(timeout)


@step(u'I show the element with id "{id}"')
@persona_vars
def show_element_by_id(context, id):
    assert context.browser.find_by_id(id)
    context.browser.execute_script('document.getElementById("%s").style.display="inline";' % id)


@step(u'I hide the element with id "{id}"')
@persona_vars
def hide_element_by_id(context, id):
    assert context.browser.find_by_id(id)
    context.browser.execute_script('document.getElementById("%s").style.display="none";' % id)


@step(u'I should see "{text}"')
@persona_vars
@multiplatform
def should_see(context, text):

    def browser(context, text):
        assert context.browser.is_text_present(text), u'Text not found'

    def mobile(context, text):
        if not text_exists_on_device(context, text):
            assert False, u'Text not found. Available text: "%s"' % '", "'.join(texts_on_device(context))


@step(u'I should see "{text}" inside the element with id "{id}" within {timeout:d} seconds')
@persona_vars
@multiplatform
def should_see_timeout(context, text, id, timeout):

    def mobile(context, text, id, timeout):
        assert _retry(lambda: text_exists_on_device(context, text, id), timeout), \
            u'Text %s not found. Available text: "%s"' % (text, '", "'.join(texts_on_device(context, id)))


@step(u'I should not see "{text}"')
@persona_vars
@multiplatform
def should_not_see(context, text):

    def browser(context, text):
        assert context.browser.is_text_not_present(text), u'Text was found'

    def mobile(context, text):
        if text_exists_on_device(context, text):
            assert False, u'Text found'


@step(u'I should see "{text}" within {timeout:d} seconds')
@persona_vars
@multiplatform
def should_see_within_timeout(context, text, timeout):

    def browser(context, text, timeout):
        assert context.browser.is_text_present(text, wait_time=timeout), u'Text not found'

    def mobile(context, text, timeout):
        assert _retry(lambda: text_exists_on_device(context, text), timeout), \
            u'Text not found. Available text: "%s"' % '", "'.join(texts_on_device(context))


@step(u'I should not see "{text}" within {timeout:d} seconds')
@persona_vars
@multiplatform
def should_not_see_within_timeout(context, text, timeout):

    def browser(context, text, timeout):
        assert context.browser.is_text_not_present(text, wait_time=timeout), u'Text was found'

    def mobile(context, text, timeout):
        assert _retry(lambda: not text_exists_on_device(context, text), timeout), u'Text was found'


@step(u'I should see an element with id "{id}"')
@persona_vars
@multiplatform
def should_see_element_with_id(context, id):

    def browser(context, id):
        assert context.browser.is_element_present_by_id(id), u'Element not found'

    def mobile(context, id):
        assert find_device_element_by_name_or_id(context, id), u'Element not found'


@step(u'I should not see an element with id "{id}"')
@persona_vars
@multiplatform
def should_not_see_element_with_id(context, id):

    def browser(context, id):
        assert context.browser.is_element_not_present_by_id(id), u'Element was found'

    def mobile(context, id):
        assert find_device_element_by_name_or_id(context, id) is None, u'Element was found'


@step(u'I should see an element with id "{id}" within {timeout:d} seconds')
@persona_vars
@multiplatform
def should_see_element_with_id_within_timeout(context, id, timeout):

    def browser(context, id, timeout):
        assert context.browser.is_element_present_by_id(id, wait_time=timeout), u'Element not found'

    def mobile(context, id, timeout):
        assert _retry(lambda: find_device_element_by_name_or_id(context, id), timeout), u'Element not found'


@step(u'I should not see an element with id "{id}" within {timeout:d} seconds')
@persona_vars
@multiplatform
def should_not_see_element_with_id_within_timeout(context, id, timeout):

    def browser(context, id, timeout):
        assert context.browser.is_element_not_present_by_id(id, wait_time=timeout), u'Element was found'

    def mobile(context, id, timeout):
        assert _retry(lambda: not find_device_element_by_name_or_id(context, id), timeout), u'Element was found'


@step(u'I should see an element with the css selector "{css}"')
def should_see_element_with_css(context, css):
    assert context.browser.is_element_present_by_css(css), u'Element not found'


@step(u'I should not see an element with the css selector "{css}"')
def should_not_see_element_with_css(context, css):
    assert context.browser.is_element_not_present_by_css(css), u'Element was found'


@step(u'I should see an element with the css selector "{css}" within {timeout:d} seconds')
def should_see_element_with_css_within_timeout(context, css, timeout):
    assert context.browser.is_element_present_by_css(css, wait_time=timeout), u'Element not found'


@step(u'I should not see an element with the css selector "{css}" within {timeout:d} seconds')
def should_not_see_element_with_css_within_timeout(context, css, timeout):
    assert context.browser.is_element_not_present_by_css(css, wait_time=timeout), u'Element was found'


@step(u'I should see {n:d} elements with the css selector "{css}"')
def should_see_n_elements_with_css(context, n, css):
    element_list = context.browser.find_by_css(css)
    list_length = len(element_list)
    assert list_length == n, u'Found {list_length} elements, expected {n}'.format(**locals())


@step(u'I should see at least {n:d} elements with the css selector "{css}" within {timeout:d} seconds')
def should_see_at_least_n_elements_with_css_within_timeout_seconds(context, n, css, timeout):

    def _check():
        element_list = context.browser.find_by_css(css)
        list_length = len(element_list)
        return list_length >= n

    assert _retry(_check, timeout), 'Did not find %s elements within %s seconds' % (n, timeout)


@step(u'I should see an element with xpath "{xpath}"')
@persona_vars
@multiplatform
def should_see_element_with_xpath(context, xpath):

    def browser(context, xpath):
        assert context.browser.is_element_present_by_xpath(xpath), u'Element not found'

    def mobile(context, xpath):
        try:
            context.device.find_element_by_xpath(xpath)
        except NoSuchElementException:
            assert False, u'Element not found'


@step(u'I should not see an element with xpath "{xpath}"')
@persona_vars
@multiplatform
def should_not_see_element_with_xpath(context, xpath):

    def browser(context, xpath):
        assert context.browser.is_element_not_present_by_xpath(xpath), u'Element was found'

    def mobile(context, xpath):
        try:
            context.device.find_element_by_xpath(xpath),
            assert False, u'Element was found'
        except NoSuchElementException:
            pass


@step(u'I should see an element with xpath "{xpath}" within {timeout:d} seconds')
@persona_vars
@multiplatform
def should_see_element_with_xpath_within_timeout(context, xpath, timeout):

    def browser(context, xpath, timeout):
        assert context.browser.is_element_present_by_xpath(xpath, wait_time=timeout), u'Element not found'

    def mobile(context, xpath, timeout):
        assert _retry(lambda: context.device.find_element_by_xpath(xpath), timeout), u'Element not found'


@step(u'I should not see an element with xpath "{xpath}" within {timeout:d} seconds')
@persona_vars
@multiplatform
def should_not_see_element_with_xpath_within_timeout(context, xpath, timeout):

    def browser(context, xpath, timeout):
        assert context.browser.is_element_not_present_by_xpath(xpath, wait_time=timeout), u'Element was found'

    def mobile(context, xpath, timeout):
        assert _retry(lambda: not context.device.find_element_by_xpath(xpath), timeout), u'Element was found'


@step(u'I execute the script "{script}"')
def execute_script(context, script):
    context.browser.execute_script(script)


@step(u'I evaluate the script "{script}" and assign the result to "{key}"')
def evaluate_script(context, script, key):
    assert context.persona is not None, u'no persona is setup'
    context.persona[key] = context.browser.evaluate_script(script)
