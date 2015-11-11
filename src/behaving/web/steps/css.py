from behave import step
from .basic import _retry

#@step(u'I should find an element with css "{css}"')
@step(u'I should see an element with the css selector "{css}"') # deprecated
def should_see_element_with_css(context, css):
    assert context.browser.is_element_present_by_css(css), u'Element not found'


#@step(u'I should not find an element with css "{css}"')
@step(u'I should not see an element with the css selector "{css}"') # deprecated
def should_not_see_element_with_css(context, css):
    assert context.browser.is_element_not_present_by_css(css), u'Element was found'


#@step(u'I should find an element with css "{css}" within {timeout:d} seconds')
@step(u'I should see an element with the css selector "{css}" within {timeout:d} seconds') # deprecated
def should_see_element_with_css_within_timeout(context, css, timeout):
    assert context.browser.is_element_present_by_css(css, wait_time=timeout), u'Element not found'


#@step(u'I should not find an element with css "{css}" within {timeout:d} seconds')
@step(u'I should not see an element with the css selector "{css}" within {timeout:d} seconds') # deprecated
def should_not_see_element_with_css_within_timeout(context, css, timeout):
    assert context.browser.is_element_not_present_by_css(css, wait_time=timeout), u'Element was found'


#@step(u'I should find {n:d} elements with css "{css}"')
@step(u'I should see {n:d} elements with the css selector "{css}"') # deprecated
def should_see_n_elements_with_css(context, n, css):
    element_list = context.browser.find_by_css(css)
    list_length = len(element_list)
    assert list_length == n, u'Found {list_length} elements, expected {n}'.format(**locals())


#@step(u'I should find at least {n:d} elements with css "{css}" within {timeout:d} seconds')
@step(u'I should see at least {n:d} elements with the css selector "{css}" within {timeout:d} seconds') # deprecated
def should_see_at_least_n_elements_with_css_within_timeout_seconds(context, n, css, timeout):
    def _check():
        element_list = context.browser.find_by_css(css)
        list_length = len(element_list)
        return list_length >= n
    assert _retry(_check, timeout), 'Did not find %s elements within %s seconds' % (n, timeout)



# my new steps


def elements_visible_css(context, css):
    ''' Finds visible elements using a CSS selector and wait_time. '''
    return [elem for elem in context.browser.find_by_css(css) if elem.visible]

def _should_see_element_visible(context, css, timeout):
    check = lambda: len(elements_visible_css(context, css)) > 0
    assert _retry(check, timeout), u"Element not visible"

def _should_not_see_element_visible(context, css, timeout):
    check = lambda: len(elements_visible_css(context, css)) == 0
    assert _retry(check, timeout), u"Unexpectedly found visible element(s)"

def _should_see_n_elements_visible(context, expected, css, timeout):
    check = lambda: len(elements_visible_css(context, css)) == expected
    assert _retry(check, timeout), u"Didn't find exactly %d visible elements" % (expected,)

def _should_see_gte_n_elements_visible(context, expected, css, timeout):
    check = lambda: len(elements_visible_css(context, css)) >= expected
    assert _retry(check, timeout), u"Didn't find at least %d visible elements" % (expected,)


@step(u'I should see an element visible with css "{css}"')
def should_see_element_visible_with_css(context, css):
    _should_see_element_visible(context, css, context.browser.wait_time)

@step(u'I should see an element visible with css "{css}" within {timeout:d} seconds')
def should_see_element_visible_with_css_within_timeout(context, css, timeout):
    _should_see_element_visible(context, css, timeout)

@step(u'I should not see an element visible with css "{css}"')
def should_not_see_element_visible_with_css(context, css):
    _should_not_see_element_visible(context, css, context.browser.wait_time)
    
@step(u'I should not see an element visible with css "{css}" within {timeout:d} seconds')
def should_not_see_element_visible_with_css_within_timeout(context, css, timeout):
    _should_not_see_element_visible(context, css, timeout)

@step(u'I should see {n:d} elements visible with css "{css}"')
def should_see_n_elements_visible_with_css(context, n, css):
    _should_see_n_elements_visible(context, n, css, context.browser.wait_time)

@step(u'I should see {n:d} elements visible with css "{css}" within {timeout:d} seconds')
def should_see_n_elements_visible_with_css_within_timeout(context, n, css, timeout):
    _should_see_n_elements_visible(context, n, css, timeout)

@step(u'I should see at least {n:d} elements visible with css "{css}"')
def should_see_gte_n_elements_visible_with_css(context, n, css):
    _should_see_gte_n_elements_visible(context, n, css, context.browser.wait_time)

@step(u'I should see at least {n:d} elements visible with css "{css}" within {timeout:d} seconds')
def should_see_gte_n_elements_visible_with_css_within_timeout(context, n, css, timeout):
    _should_see_gte_n_elements_visible(context, n, css, timeout)