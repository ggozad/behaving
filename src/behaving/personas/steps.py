from behave import given, when, then

from behaving.personas.persona import Persona
from behaving.personas.persona import persona_vars


@given('"{name}" as the persona')
def given_a_persona(context, name):

    if name not in context.personas:
        context.personas[name] = Persona()
    context.persona = context.personas[name]

    if hasattr(context, 'browser'):
        context.execute_steps('Given "%s" as the browser' % name)


@when('I set "{key}" to "{val}"')
def set_variable(context, key, val):
    assert context.persona is not None
    context.persona[key] = val


@then('"{key}" is set to "{val}"')
@persona_vars
def key_is_val(context, key, val):
    assert context.persona
    assert key in context.persona
    assert context.persona[key] == val
