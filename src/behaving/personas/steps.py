from behave import given, when, then

from behaving.personas.persona import Persona
from behaving.personas.persona import persona_vars


@given(u'"{name}" as the persona')
def given_a_persona(context, name):

    if name not in context.personas:
        context.personas[name] = Persona()
    context.persona = context.personas[name]

    if hasattr(context, 'browser'):
        context.execute_steps('Given browser "%s"' % name)


@when(u'I set "{key}" to "{val}"')
def set_variable(context, key, val):
    assert context.persona is not None, u'no persona is setup'
    context.persona[key] = val


@then(u'"{key}" is set to "{val}"')
@persona_vars
def key_is_val(context, key, val):
    assert context.persona is not None, u'no persona is setup'
    assert key in context.persona, u'key not set'
    assert context.persona[key] == val, u'values do not match'
