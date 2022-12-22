from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from behave import then, when

from behaving.personas.persona import persona_vars
from behaving.utils import parse_text


@when('I set "{key}" to the body of the sms I received at "{tel}"')
@persona_vars
def set_var_to_sms_body(context, key, tel):
    assert context.persona is not None, "No persona is setup"
    msgs = context.sms.user_messages(tel)
    assert msgs, f"No sms received at {tel}"
    context.persona[key] = msgs[-1]


@when('I parse the sms I received at "{tel}" and set "{expression}"')
@persona_vars
def parse_sms_set_var(context, tel, expression):
    assert context.persona is not None, "No persona is setup"
    msgs = context.sms.user_messages(tel)
    assert msgs, f"No sms received at {tel}"
    msg = msgs[-1]
    parse_text(context, msg, expression)


@then('I should receive an sms at "{tel}" containing "{text}"')
@persona_vars
def should_receive_sms_with_text(context, tel, text):
    msgs = context.sms.user_messages(tel)
    for msg in msgs:
        if text in msg:
            return
    assert False, f'Text "{text}" not found in {tel} sms.'


@then('I should receive an sms at "{tel}"')
@persona_vars
def should_receive_sms(context, tel):
    assert context.sms.user_messages(tel), f"Sms not received at {tel}"


@when('I send an sms to "{to}" with body "{body}"')
@persona_vars
def send_sms(context, to, body):
    url = "http://localhost:8199"
    values = {"from": "TEST", "to": to, "text": body}

    data = urlencode(values)
    req = Request(url, data.encode("utf-8"))
    try:
        urlopen(req)
    except HTTPError:
        assert "Could not send sms"
