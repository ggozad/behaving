from behave import step

from behaving.personas.persona import Persona
from behaving.personas.persona import persona_vars


@step(u'"{name}" as the persona')
def given_a_persona(context, name):

    if name not in context.personas:
        context.personas[name] = Persona()
    context.persona = context.personas[name]

    single_browser = hasattr(context, "single_browser")
    if hasattr(context, "browser"):
        if single_browser and hasattr(context, "is_connected"):
            return
    context.execute_steps('Given browser "%s"' % name)
    if single_browser:
        context.is_connected = True


@step(u'I set "{key}" to "{val}"')
@persona_vars
def set_variable(context, key, val):
    assert context.persona is not None, u"no persona is setup"
    context.persona[key] = val


@step(u'I set "{key}" to')
@persona_vars
def set_variable_text(context, key):
    assert context.persona is not None, u"no persona is setup"
    context.persona[key] = context.text


@step(u'"{key}" is set to "{val}"')
@persona_vars
def key_is_val(context, key, val):
    assert context.persona is not None, u"no persona is setup"
    assert context.persona[key] == val, u"%s != %s, values do not match" % (
        context.persona[key],
        val,
    )


@step(u'"{key}" is a dictionary')
@persona_vars
def key_is_dict(context, key):
    assert context.persona is not None, u"no persona is setup"
    assert type(context.persona[key]) == dict, u"%s is not a dictionary" % type(key)


@step(u'I clone persona "{source}" to "{target}"')
def clone_persona(context, source, target):
    assert source in context.personas, u"Persona %s does not exist" % source
    if target not in context.personas:
        context.personas[target] = Persona(context.personas.get(source))
