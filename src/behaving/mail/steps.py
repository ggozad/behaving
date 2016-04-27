import email
from email.header import decode_header
from email.mime.base import MIMEBase
from email.header import Header
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import os.path
import quopri
from behave import step
from behaving.personas.persona import persona_vars


MAIL_TIMEOUT = 5
URL_RE = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|\
                    (?:%[0-9a-fA-F][0-9a-fA-F]))+', re.I | re.S | re.U)


@step(u'I should receive an email at "{address}" containing "{text}"')
@persona_vars
def should_receive_email_containing_text(context, address, text):
    def filter_contents(mail):
        mail = email.message_from_string(mail)
        return text in quopri.decodestring(mail.get_payload()).decode('utf-8')

    assert context.mail.user_messages(address, filter_contents)


@step(u'I should receive an email at "{address}" with subject "{subject}"')
@persona_vars
def should_receive_email_with_subject(context, address, subject):
    def get_subject_from_mail(mail):
        text, encoding = decode_header(mail.get('Subject'))[0]
        return text.decode(encoding) if encoding else text

    def filter_contents(mail):
        mail = email.message_from_string(mail)
        return subject == get_subject_from_mail(mail)

    assert context.mail.user_messages(address, filter_contents), u'message not found'


@step(u'I should receive an email at "{address}" with attachment "{filename}"')
@persona_vars
def should_receive_email_with_attachment(context, address, filename):
    def filter_contents(mail):
        mail = email.message_from_string(mail)
        if len(mail.get_payload()) > 1:
            attachments = mail.get_payload()
            for attachment in attachments:
                if filename == attachment.get_filename():
                    return True
            return False

    assert context.mail.user_messages(address, filter_contents), u'message not found'


@step(u'I should receive an email at "{address}"')
@persona_vars
def should_receive_email(context, address):
    assert context.mail.user_messages(address), u'message not found'


@step(u'I click the link in the email I received at "{address}"')
@persona_vars
def click_link_in_email(context, address):
    mails = context.mail.user_messages(address)
    assert mails, u'message not found'
    mail = email.message_from_string(mails[-1])
    links = URL_RE.findall(str(mail).replace('=\n', ''))
    assert links, u'link not found'
    url = links[0]
    context.browser.visit(url)


@step(u'I parse the email I received at "{address}" and set "{expression}"')
@persona_vars
def parse_email_set_var(context, address, expression):
    assert context.persona is not None, u'no persona is setup'
    msgs = context.mail.user_messages(address)
    assert msgs, u'no email received'
    mail = email.message_from_string(msgs[-1])
    text = quopri.decodestring(mail.get_payload()).decode("utf-8")
    parse_text(context, text, expression)


def parse_text(context, text, expression):
    import parse
    parser = parse.compile(expression)
    res = parser.parse(text)

    # Make an implicit assumption that there might be something before the expression
    if res is None:
        expr = '{}' + expression
        parser = parse.compile(expr)
        res = parser.parse(text)

    # Make an implicit assumption that there might be something after the expression
    if res is None:
        expr = expression + '{}'
        parser = parse.compile(expr)
        res = parser.parse(text)

    # Make an implicit assumption that there might be something before/after the expression
    if res is None:
        expr = '{}' + expression + '{}'
        parser = parse.compile(expr)
        res = parser.parse(text)

    assert res, u'expression not found'
    assert res.named, u'expression not found'
    for key, val in res.named.items():
        context.persona[key] = val


@step('I send an email to "{to}" with subject "{subject}" and body "{body}" and attachment "{filename}"')
def send_email_attachment(context, to, subject, body, filename):
    msg = MIMEMultipart(From='test@localhost',
                        To=to)
    msg['Subject'] = Header(subject, 'utf-8')
    msg.attach(MIMEText(body))
    path = os.path.join(context.attachment_dir, filename)
    with open(path, 'rb') as fil:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(fil.read())
        attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(filename))
        msg.attach(attachment)

    s = smtplib.SMTP('localhost', 8025)
    s.sendmail('test@localhost', [to], msg.as_string())
    s.quit()


@step('I send an email to "{to}" with subject "{subject}" and body "{body}"')
def send_email(context, to, subject, body):
    msg = MIMEText(body.encode('utf-8'))
    msg['Subject'] = Header(subject.encode('utf-8'), 'utf-8')
    msg['To'] = to
    msg['From'] = 'test@localhost'
    s = smtplib.SMTP('localhost', 8025)
    s.sendmail('test@localhost', [to], msg.as_string())
    s.quit()
