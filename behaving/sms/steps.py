from behave import then


@then('I should receive an sms at {tel} containing "{text}"')
def should_receive_sms_with_text(context, tel, text):
    msgs = context.sms.user_messages(tel)
    for msg in msgs:
        if text in msg:
            return
    assert False, 'Text not found'


@then('I should receive an sms at {tel}')
def should_receive_sms(context, tel):
    assert context.sms.user_messages(tel)
