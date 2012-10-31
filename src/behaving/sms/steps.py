from behave import when, then
import parse
from behaving.personas.persona import persona_vars


@then('I set "{key}" to the body of the sms I received at "{tel}"')
@persona_vars
def set_var_to_sms_body(context, key, tel):
    assert context.persona is not None
    msgs = context.sms.user_messages(tel)
    assert msgs
    context.persona[key] = msgs[-1]


@when('I parse the sms I received at "{tel}" and set "{expression}"')
@persona_vars
def parse_sms_set_var(context, tel, expression):
    assert context.persona is not None
    msgs = context.sms.user_messages(tel)
    assert msgs

    parser = parse.compile(expression)
    res = parser.parse(msgs[-1])

    # Make an implicit assumption that there might be something before/after the expression
    if res is None:
        expression = '{}' + expression + '{}'
        parser = parse.compile(expression)
        res = parser.parse(msgs[-1])

    assert res
    assert res.named
    for key, val in res.named.items():
        context.persona[key] = val


@then('I should receive an sms at "{tel}" containing "{text}"')
@persona_vars
def should_receive_sms_with_text(context, tel, text):
    print tel
    msgs = context.sms.user_messages(tel)
    for msg in msgs:
        if text in msg:
            return
    assert False, 'Text not found'


@then('I should receive an sms at "{tel}"')
@persona_vars
def should_receive_sms(context, tel):
    assert context.sms.user_messages(tel)
