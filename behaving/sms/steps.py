from behave import then
import time

SMS_TIMEOUT = 5


def filter_messages(context, address, f=None):
    messages = []
    start = time.time()
    while time.time() - start < SMS_TIMEOUT:
        messages = filter(f, context.sms.messages_for_user(address))
        if messages:
            break
        time.sleep(0.2)
    return messages


@then('I should receive an sms at {tel}')
def should_receive_sms(context, tel):
    assert filter_messages(context, tel)
