try:
    from urllib import urlencode
    from urllib2 import Request, urlopen, HTTPError
except ImportError:
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError
import smtplib
from email.mime.text import MIMEText
from behave import when
from behave import step

from behaving.web.steps import *
from behaving.sms.steps import *
from behaving.mail.steps import *
from behaving.mobile.steps import *
from behaving.personas.steps import *
from behaving.personas.persona import persona_vars


@when('I send an sms to "{to}" with body "{body}"')
@persona_vars
def send_sms(context, to, body):
    url = 'http://localhost:8199'
    values = {'from': 'TEST',
              'to': to,
              'text': body}

    data = urlencode(values)
    req = Request(url, data.encode('utf-8'))
    try:
        urlopen(req)
    except HTTPError:
        assert False


@when('I send an email to "{to}" with subject "{subject}" and body "{body}"')
@persona_vars
def send_email(context, to, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['To'] = to
    msg['From'] = 'test@localhost'
    s = smtplib.SMTP('localhost', 8025)
    s.sendmail('test@localhost', [to], msg.as_string())
    s.quit()


@step('"{key}" has property "{propname}"')
@persona_vars
def persona_var_has_property(context, key, propname):
    assert hasattr(context.persona, key) or context.persona.has_key(key), "context.persona[%s] does not have property %s" % (key, propname)