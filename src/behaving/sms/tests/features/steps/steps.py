import urllib
import urllib2

from behave import when
from behaving.sms.steps import *


@when('I send an sms to {to} with body "{body}"')
def send_sms(context, to, body):
    url = 'http://localhost:8099'
    values = {'from': 'TEST',
              'to': to,
              'body': body}

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    try:
        urllib2.urlopen(req)
    except HTTPError:
        assert False
