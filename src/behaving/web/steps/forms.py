import os
from behave import step
from behaving.personas.persona import persona_vars


@step(u'I fill in "{name}" with "{value}"')
@persona_vars
def i_fill_in_field(context, name, value):
    context.browser.fill(name, value)


@step(u'I type "{value}" to "{name}"')
@persona_vars
def i_type_to(context, name, value):
    for key in context.browser.type(name, value, slowly=True):
        assert key


@step(u'I choose "{value}" from "{name}"')
@persona_vars
def i_choose_in_radio(context, name, value):
    context.browser.choose(name, value)


@step(u'I check "{name}"')
@persona_vars
def i_check(context, name):
    context.browser.check(name)


@step(u'I uncheck "{name}"')
@persona_vars
def i_uncheck(context, name):
    context.browser.uncheck(name)


@step(u'I select "{value}" from "{name}"')
@persona_vars
def i_select(context, value, name):
    context.browser.select(name, value)


@step(u'I press "{name}"')
@persona_vars
def i_press(context, name):
    button = \
        context.browser.find_by_id(name) or \
        context.browser.find_by_name(name) or \
        context.browser.find_by_xpath("//button[text()='%s']" % name) or \
        context.browser.find_by_xpath("//button[contains(text(), '%s')]" % name) or \
        context.browser.find_link_by_text(name) or \
        context.browser.find_link_by_partial_text(name)
    assert button, u'Element not found'
    button.first.click()


@step(u'I press the element with xpath "{xpath}"')
@persona_vars
def i_press_xpath(context, xpath):
    button = context.browser.find_by_xpath(xpath)
    assert button, u'Element not found'
    button.first.click()


@step('I attach the file "{path}" to "{name}"')
@persona_vars
def i_attach(context, name, path):
    if not os.path.exists(path):
        path = os.path.join(context.attachment_dir, path)
        if not os.path.exists(path):
            assert False
    context.browser.attach_file(name, path)


@step('I set the inner HTML of the element with id "{id}" to "{contents}"')
@persona_vars
def set_html_content_to_element_with_id(context, id, contents):
    assert context.browser.evaluate_script("document.getElementById('%s').innerHTML = '%s'" % (id, contents)), u'Element not found or could not set HTML content'


@step('I set the inner HTML of the element with class "{klass}" to "{contents}"')
@persona_vars
def set_html_content_to_element_with_class(context, klass, contents):
    assert context.browser.evaluate_script("document.getElementsByClassName('%s')[0].innerHTML = '%s'" % (klass, contents)), u'Element not found or could not set HTML content'


@step(u'field "{name}" should have the value "{value}"')
@persona_vars
def field_has_value(context, name, value):
    el = context.browser.find_by_id(name) or context.browser.find_by_name(name)
    assert el, u'Element not found'
    assert el.first.value == value, "Values do not match"


@step(u'"{name}" should be enabled')
@persona_vars
def is_enabled(context, name):
    el = context.browser.find_by_id(name) or context.browser.find_by_name(name)
    assert el, u'Element not found'
    assert el.first._element.is_enabled()


@step(u'"{name}" should be disabled')
@step(u'"{name}" should not be enabled')
@persona_vars
def is_disabled(context, name):
    el = context.browser.find_by_id(name) or context.browser.find_by_name(name)
    assert el, u'Element not found'
    assert not el.first._element.is_enabled()


@step(u'field "{name}" should be valid')
@persona_vars
def field_is_valid(context, name):
    assert context.browser.find_by_name(name), u'Element not found'
    assert context.browser.evaluate_script("document.getElementsByName('%s')[0].checkValidity()" % name), \
        'Field is invalid'


@step(u'field "{name}" should be invalid')
@step(u'field "{name}" should not be valid')
@persona_vars
def field_is_invalid(context, name):
    assert context.browser.find_by_name(name), u'Element not found'
    assert not context.browser.evaluate_script("document.getElementsByName('%s')[0].checkValidity()" % name), \
        'Field is valid'


@step(u'field "{name}" should be required')
@persona_vars
def field_is_required(context, name):
    assert context.browser.find_by_name(name), u'Element not found'
    assert context.browser.evaluate_script("document.getElementsByName('%s')[0].getAttribute('required')" % name), \
        'Field is not required'


@step(u'field "{name}" should not be required')
@persona_vars
def field_is_not_required(context, name):
    assert context.browser.find_by_name(name), u'Element not found'
    assert not context.browser.evaluate_script("document.getElementsByName('%s')[0].getAttribute('required')" % name), \
        'Field is required'
