import parse
from behave import step
from behaving.personas.persona import persona_vars


@step(u'I set "{key}" to the body of the sms I received at "{tel}"')
@persona_vars
def set_var_to_sms_body(context, key, tel):
    assert context.persona is not None
    msgs = context.sms.user_messages(tel)
    assert msgs
    context.persona[key] = msgs[-1]


@step(u'I parse the sms I received at "{tel}" and set "{expression}"')
@persona_vars
def parse_sms_set_var(context, tel, expression):
    assert context.persona is not None, u'no persona is setup'
    msgs = context.sms.user_messages(tel)
    assert msgs, u'no sms received'

    parser = parse.compile(expression)
    res = parser.parse(msgs[-1])

    # Make an implicit assumption that there might be something before/after the expression
    if res is None:
        expression = '{}' + expression + '{}'
        parser = parse.compile(expression)
        res = parser.parse(msgs[-1])

    assert res, u'expression not found'
    assert res.named, u'expression not found'
    for key, val in res.named.items():
        context.persona[key] = val


@step(u'I should receive an sms at "{tel}" containing "{text}"')
@persona_vars
def should_receive_sms_with_text(context, tel, text):
    msgs = context.sms.user_messages(tel)
    for msg in msgs:
        if text in msg:
            return
    assert False, u'Text not found in sms'


@step(u'I should receive an sms at "{tel}"')
@persona_vars
def should_receive_sms(context, tel):
    assert context.sms.user_messages(tel), u'sms not received'
