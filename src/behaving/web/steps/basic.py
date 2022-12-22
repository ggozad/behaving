import time

from behave import then, when

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


@when("I wait for {timeout:d} seconds")
@persona_vars
def wait_for_timeout(context, timeout):
    time.sleep(timeout)


@when('I show the element with id "{id}"')
@persona_vars
def show_element_by_id(context, id):
    assert context.browser.find_by_id(id), f"Element with id {id} not found"
    context.browser.execute_script(
        f'document.getElementById("{id}").style.display="inline";'
    )


@when('I hide the element with id "{id}"')
@persona_vars
def hide_element_by_id(context, id):
    assert context.browser.find_by_id(id), f"Element with id {id} not found"
    context.browser.execute_script(
        f'document.getElementById("{id}").style.display="none";'
    )


@then('I should see "{text}"')
@then('I should see "{text}" within {timeout:d} seconds')
@persona_vars
def should_see_within_timeout(context, text, timeout=None):
    assert context.browser.is_text_present(
        text, wait_time=timeout
    ), f'Text "{text}" not found'


@then('I should not see "{text}"')
@then('I should not see "{text}" within {timeout:d} seconds')
@persona_vars
def should_not_see_within_timeout(context, text, timeout=None):
    assert context.browser.is_text_not_present(
        text, wait_time=timeout
    ), f'Text "{text}" was found'


@then('I should see an element with id "{id}"')
@then('I should see an element with id "{id}" within {timeout:d} seconds')
@persona_vars
def should_see_element_with_id_within_timeout(context, id, timeout=None):
    assert context.browser.is_element_present_by_id(
        id, wait_time=timeout
    ), f'Element with id "{id}" not found'


@then('I should not see an element with id "{id}"')
@then('I should not see an element with id "{id}" within {timeout:d} seconds')
@persona_vars
def should_not_see_element_with_id_within_timeout(context, id, timeout=None):
    assert context.browser.is_element_not_present_by_id(
        id, wait_time=timeout
    ), f'Element with id "{id}" was found'


@then('I should see an element with xpath "{xpath}"')
@then('I should see an element with xpath "{xpath}" within {timeout:d} seconds')
@persona_vars
def should_see_element_with_xpath_within_timeout(context, xpath, timeout=None):
    assert context.browser.is_element_present_by_xpath(
        xpath, wait_time=timeout
    ), f'Element with xpath "{xpath}" not found'


@then('I should not see an element with xpath "{xpath}"')
@then('I should not see an element with xpath "{xpath}" within {timeout:d} seconds')
@persona_vars
def should_not_see_element_with_xpath_within_timeout(context, xpath, timeout=None):
    assert context.browser.is_element_not_present_by_xpath(
        xpath, wait_time=timeout
    ), f'Element with xpath "{xpath}" was found'


@when('I execute the script "{script}"')
def execute_script(context, script):
    context.browser.execute_script(script)


@when('I evaluate the script "{script}" and assign the result to "{key}"')
def evaluate_script(context, script, key):
    assert context.persona is not None, "No persona is setup"
    context.persona[key] = context.browser.evaluate_script(script)
