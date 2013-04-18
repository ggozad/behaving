from behave import step

from behaving.personas.persona import Persona
from behaving.personas.persona import persona_vars


@step(u'"{name}" as the persona')
def given_a_persona(context, name):

    if name not in context.personas:
        context.personas[name] = Persona()
    context.persona = context.personas[name]

    if hasattr(context, 'browser'):
        context.execute_steps('Given browser "%s"' % name)


@step(u'I set "{key}" to "{val}"')
@persona_vars
def set_variable(context, key, val):
    assert context.persona is not None, u'no persona is setup'
    context.persona[key] = val


@step(u'"{key}" is set to "{val}"')
@persona_vars
def key_is_val(context, key, val):
    assert context.persona is not None, u'no persona is setup'
    assert key in context.persona, u'key not set'
    assert context.persona[key] == val, u'%s != %s, values do not match' % (context.persona[key], val)
