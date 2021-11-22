import time
from behave import step

from behaving.personas.persona import persona_vars


# Accepts a lambda as first paramter, returns lambda result on success, or False on timeout
def _retry(func, timeout=0, delay=1):
    assert isinstance(
        func, type(lambda: None)
    ), "Retry expects a lambda as the first argument"

    start = time.time()
    while True:
        try:
            res = func()
            if not res:
                time.sleep(delay)
            else:
                return res
        except Exception:
            time.sleep(delay)

        if time.time() - start > timeout:
            return None


@step(u"I wait for {timeout:d} seconds")
@persona_vars
def wait_for_timeout(context, timeout):
    time.sleep(timeout)


@step(u'I show the element with id "{id}"')
@persona_vars
def show_element_by_id(context, id):
    assert context.browser.find_by_id(id)
    context.browser.execute_script(
        'document.getElementById("%s").style.display="inline";' % id
    )


@step(u'I hide the element with id "{id}"')
@persona_vars
def hide_element_by_id(context, id):
    assert context.browser.find_by_id(id)
    context.browser.execute_script(
        'document.getElementById("%s").style.display="none";' % id
    )


@step(u'I should see "{text}"')
@persona_vars
def should_see(context, text):
    assert context.browser.is_text_present(text), u'Text "%s" not found' % text


@step(u'I should not see "{text}"')
@persona_vars
def should_not_see(context, text):
    assert context.browser.is_text_not_present(text), u'Text "%s" was found' % text


@step(u'I should see "{text}" within {timeout:d} seconds')
@persona_vars
def should_see_within_timeout(context, text, timeout):
    assert context.browser.is_text_present(text, wait_time=timeout), (
        u'Text "%s" not found' % text
    )


@step(u'I should not see "{text}" within {timeout:d} seconds')
@persona_vars
def should_not_see_within_timeout(context, text, timeout):
    assert context.browser.is_text_not_present(text, wait_time=timeout), (
        u'Text "%s" was found' % text
    )


@step(u'I should see an element with id "{id}"')
@persona_vars
def should_see_element_with_id(context, id):
    assert context.browser.is_element_present_by_id(id), u"Element not found"


@step(u'I should not see an element with id "{id}"')
@persona_vars
def should_not_see_element_with_id(context, id):
    assert context.browser.is_element_not_present_by_id(id), u"Element was found"


@step(u'I should see an element with id "{id}" within {timeout:d} seconds')
@persona_vars
def should_see_element_with_id_within_timeout(context, id, timeout):
    assert context.browser.is_element_present_by_id(
        id, wait_time=timeout
    ), u"Element not found"


@step(u'I should not see an element with id "{id}" within {timeout:d} seconds')
@persona_vars
def should_not_see_element_with_id_within_timeout(context, id, timeout):
    assert context.browser.is_element_not_present_by_id(
        id, wait_time=timeout
    ), u"Element was found"


@step(u'I should see an element with xpath "{xpath}"')
@persona_vars
def should_see_element_with_xpath(context, xpath):
    assert context.browser.is_element_present_by_xpath(xpath), u"Element not found"


@step(u'I should not see an element with xpath "{xpath}"')
@persona_vars
def should_not_see_element_with_xpath(context, xpath):
    assert context.browser.is_element_not_present_by_xpath(xpath), u"Element was found"


@step(u'I should see an element with xpath "{xpath}" within {timeout:d} seconds')
@persona_vars
def should_see_element_with_xpath_within_timeout(context, xpath, timeout):
    assert context.browser.is_element_present_by_xpath(
        xpath, wait_time=timeout
    ), u"Element not found"


@step(u'I should not see an element with xpath "{xpath}" within {timeout:d} seconds')
@persona_vars
def should_not_see_element_with_xpath_within_timeout(context, xpath, timeout):
    assert context.browser.is_element_not_present_by_xpath(
        xpath, wait_time=timeout
    ), u"Element was found"


@step(u'I execute the script "{script}"')
def execute_script(context, script):
    context.browser.execute_script(script)


@step(u'I evaluate the script "{script}" and assign the result to "{key}"')
def evaluate_script(context, script, key):
    assert context.persona is not None, u"no persona is setup"
    context.persona[key] = context.browser.evaluate_script(script)
