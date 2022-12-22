from behave import given, then, when

from behaving.personas.persona import Persona, persona_vars


@given('"{name}" as the persona')
def given_a_persona(context, name):

    if name not in context.personas:
        context.personas[name] = Persona()
    context.persona = context.personas[name]
    context.execute_steps(f'Given browser "{name}"')


@when('I set "{key}" to "{val}"')
@persona_vars
def set_variable(context, key, val):
    assert context.persona is not None, "No persona is setup"
    context.persona[key] = val


@when('I set "{key}" to')
@persona_vars
def set_variable_text(context, key):
    assert context.persona is not None, "No persona is setup"
    context.persona[key] = context.text


@then('"{key}" is set to "{val}"')
@persona_vars
def key_is_val(context, key, val):
    assert context.persona is not None, "No persona is setup"
    assert (
        context.persona[key] == val
    ), f"{context.persona[key]} != {val}, values do not match"


@then('"{key}" is a dictionary')
@persona_vars
def key_is_dict(context, key):
    assert context.persona is not None, "no persona is setup"
    assert type(context.persona[key]) == dict, f"{type(key)} is not a dictionary"


@when('I clone persona "{source}" to "{target}"')
def clone_persona(context, source, target):
    assert source in context.personas, f"Persona {source} does not exist"
    if target not in context.personas:
        context.personas[target] = Persona(context.personas.get(source))
