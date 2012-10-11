from behave import when


@when('I fill in "{name:w}" with "{value}"')
def i_fill_in_field(context, name, value):
    context.browser.fill(name, value)


@when('I choose "{value:w}" from "{name:w}"')
def i_choose_in_radio(context, name, value):
    context.browser.choose(name, value)


@when('I check "{name:w}"')
def i_check(context, name):
    context.browser.check(name)


@when('I uncheck "{name:w}"')
def i_uncheck(context, name):
    context.browser.uncheck(name)


@when('I select "{value:w}" from "{name:w}"')
def i_select(context, value, name):
    context.browser.select(name, value)


@when('I press "{name}"')
def when_i_press(context, name):
    button = context.browser.find_by_id(name) or \
             context.browser.find_by_name(name) or \
             context.browser.find_link_by_text(name)
    assert button
    button.first.click()
