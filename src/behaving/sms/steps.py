from behave import when, then


@when('I set "{key}" to the body of the sms I received at "{tel}"')
def set_var_to_sms_body(context, key, tel):
    assert context.persona is not None
    msgs = context.sms.user_messages(tel)
    assert msgs
    context.persona[key] = msgs[-1]


@then('I should receive an sms at "{tel}" containing "{text}"')
def should_receive_sms_with_text(context, tel, text):
    msgs = context.sms.user_messages(tel)
    for msg in msgs:
        if text in msg:
            return
    assert False, 'Text not found'


@then('I should receive an sms at "{tel}"')
def should_receive_sms(context, tel):
    assert context.sms.user_messages(tel)
