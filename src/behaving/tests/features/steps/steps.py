import urllib
import urllib2
import smtplib
from email.mime.text import MIMEText
from behave import when

from behaving.web.steps import *
from behaving.sms.steps import *
from behaving.mail.steps import *
from behaving.personas.steps import *
from behaving.personas.persona import persona_vars


@when('I send an sms to "{to}" with body "{body}"')
@persona_vars
def send_sms(context, to, body):
    url = 'http://localhost:8099'
    values = {'from': 'TEST',
              'to': to,
              'text': body}

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    try:
        urllib2.urlopen(req)
    except urllib2.HTTPError:
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
