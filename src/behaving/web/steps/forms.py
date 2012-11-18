import os
from behave import when, then
from behaving.personas.persona import persona_vars


@when(u'I fill in "{name}" with "{value}"')
@persona_vars
def i_fill_in_field(context, name, value):
    context.browser.fill(name, value)


@when(u'I choose "{value}" from "{name}"')
@persona_vars
def i_choose_in_radio(context, name, value):
    context.browser.choose(name, value)


@when(u'I check "{name}"')
def i_check(context, name):
    context.browser.check(name)


@when(u'I uncheck "{name}"')
def i_uncheck(context, name):
    context.browser.uncheck(name)


@when(u'I select "{value}" from "{name}"')
@persona_vars
def i_select(context, value, name):
    context.browser.select(name, value)


@when(u'I press "{name}"')
def i_press(context, name):
    button = context.browser.find_by_id(name) or \
             context.browser.find_by_name(name) or \
             context.browser.find_by_xpath("//button[text()='%s']" % name) or \
             context.browser.find_by_xpath("//button[contains(text(), '%s')]" % name) or \
             context.browser.find_link_by_text(name) or \
             context.browser.find_link_by_partial_text(name)
    assert button, u'Element not found'
    # Go figure why checking for button.first is necessary, but it seems to be for elements
    #that listen to onclick and change somehow
    if button.first:
        button.first.click()


@when('I attach the file "{path}" to "{name}"')
@persona_vars
def i_attach(context, name, path):
    if not os.path.exists(path):
        path = os.path.join(context.attachment_dir, path)
        if not os.path.exists(path):
            assert False
    context.browser.attach_file(name, path)


@then(u'"{name}" should be enabled')
def is_enabled(context, name):
    el = context.browser.find_by_id(name) or \
         context.browser.find_by_name(name)
    assert el, u'Element not found'
    assert el.first._element.is_enabled()


@then(u'"{name}" should be disabled')
def is_disabled(context, name):
    el = context.browser.find_by_id(name) or \
         context.browser.find_by_name(name)
    assert el, u'Element not found'
    assert not el.first._element.is_enabled()


@then(u'field "{name}" should be valid')
def field_is_valid(context, name):
    assert context.browser.find_by_name(name), u'Element not found'
    assert context.browser.evaluate_script("document.getElementsByName('%s')[0].checkValidity()" % name), \
        'Field is invalid'


@then(u'field "{name}" should be invalid')
@then(u'field "{name}" should not be valid')
def field_is_invalid(context, name):
    assert context.browser.find_by_name(name), u'Element not found'
    assert not context.browser.evaluate_script("document.getElementsByName('%s')[0].checkValidity()" % name), \
        'Field is valid'
