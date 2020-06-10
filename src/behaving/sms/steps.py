try:
    from urllib import urlencode
    from urllib2 import Request, urlopen, HTTPError
except ImportError:
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError

from behave import step
from behaving.personas.persona import persona_vars
from behaving.utils import parse_text


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
    assert context.persona is not None, u"no persona is setup"
    msgs = context.sms.user_messages(tel)
    assert msgs, u"no sms received"

    msg = msgs[-1]
    parse_text(context, msg, expression)


@step(u'I should receive an sms at "{tel}" containing "{text}"')
@persona_vars
def should_receive_sms_with_text(context, tel, text):
    msgs = context.sms.user_messages(tel)
    for msg in msgs:
        if text in msg:
            return
    assert False, u"Text not found in sms"


@step(u'I should receive an sms at "{tel}"')
@persona_vars
def should_receive_sms(context, tel):
    assert context.sms.user_messages(tel), u"sms not received"


@step('I send an sms to "{to}" with body "{body}"')
@persona_vars
def send_sms(context, to, body):
    url = "http://localhost:8199"
    values = {"from": "TEST", "to": to, "text": body}

    data = urlencode(values)
    req = Request(url, data.encode("utf-8"))
    try:
        urlopen(req)
    except HTTPError:
        assert False
