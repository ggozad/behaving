from behave import given
from splinter.browser import Browser


@given(u'"{name}" as the user')
def given_a_user(context, name):
    if name in context.users:
        context.browser = context.users[name]
    else:
        if context.default_browser:
            context.users[name] = Browser(context.default_browser)
        else:
            context.users[name] = Browser()
        context.browser = context.users[name]
