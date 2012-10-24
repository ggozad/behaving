from behave import given

from behaving.personas.persona import Persona


@given('"{name}" as the persona')
def given_a_persona(context, name):

    context.persona = context.personas.get(name)
    assert context.persona
    if context.default_browser:
        context.execute_steps('Given "%s" as the user' % name)
