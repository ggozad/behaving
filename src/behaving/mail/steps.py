import email
import os.path
import re
import smtplib
from email.header import Header, decode_header, make_header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from behave import then, when

from behaving.personas.persona import persona_vars

MAIL_TIMEOUT = 5
URL_RE = re.compile(
    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|\
                    (?:%[0-9a-fA-F][0-9a-fA-F]))+",
    re.I | re.S | re.U,
)


@then('I should receive an email at "{address}" containing "{text}"')
@persona_vars
def should_receive_email_containing_text(context, address, text):
    def filter_contents(mail):
        mail = email.message_from_string(mail)
        return text in mail.get_payload(decode=True).decode("utf-8")

    assert context.mail.user_messages(
        address, filter_contents
    ), f'Text "{text}" not found at {address}'


@then('I should receive an email at "{address}" with subject "{subject}"')
@persona_vars
def should_receive_email_with_subject(context, address, subject):
    def get_subject_from_mail(mail):
        text = make_header(decode_header(mail.get("Subject")))
        return str(text)

    def filter_contents(mail):
        mail = email.message_from_string(mail)
        return subject == get_subject_from_mail(mail)

    assert context.mail.user_messages(
        address, filter_contents
    ), f'Message with subject "{subject}" not found at {address}'


@then('I should receive an email at "{address}" with attachment "{filename}"')
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

    assert context.mail.user_messages(
        address, filter_contents
    ), f"Message with attachement {filename} not found at {address}"


@then('I should receive an email at "{address}"')
@persona_vars
def should_receive_email(context, address):
    assert context.mail.user_messages(address), f"Message not found at {address}"


@when('I click the link in the email I received at "{address}"')
@persona_vars
def click_link_in_email(context, address):
    mails = context.mail.user_messages(address)
    assert mails, "message not found"
    mail = email.message_from_string(mails[-1])
    links = []
    payloads = mail.get_payload(decode=True).decode("utf-8")
    if isinstance(payloads, str):
        payloads = [payloads]
    for payload in payloads:
        links.extend(URL_RE.findall(str(payload).replace("=\n", "")))
    assert links, f"Link not found at {address}"
    url = links[0]
    context.browser.visit(url)


@when('I parse the email I received at "{address}" and set "{expression}"')
@persona_vars
def parse_email_set_var(context, address, expression):
    assert context.persona is not None, "no persona is setup"
    msgs = context.mail.user_messages(address)
    assert msgs, f"No email received at {address}"
    mail = email.message_from_string(msgs[-1])
    text = mail.get_payload(decode=True).decode("utf-8")
    parse_text(context, text, expression)


def parse_text(context, text, expression):
    import parse

    parser = parse.compile(expression)
    res = parser.parse(text)

    # Make an implicit assumption that there might be something before the expression
    if res is None:
        expr = "{}" + expression
        parser = parse.compile(expr)
        res = parser.parse(text)

    # Make an implicit assumption that there might be something after the expression
    if res is None:
        expr = expression + "{}"
        parser = parse.compile(expr)
        res = parser.parse(text)

    # Make an implicit assumption that there might be something before/after the expression
    if res is None:
        expr = "{}" + expression + "{}"
        parser = parse.compile(expr)
        res = parser.parse(text)

    assert res, "expression not found"
    assert res.named, "expression not found"
    for key, val in res.named.items():
        context.persona[key] = val


@when(
    'I send an email to "{to}" with subject "{subject}" and body "{body}" and attachment "{filename}"'
)
@persona_vars
def send_email_attachment(context, to, subject, body, filename):
    msg = MIMEMultipart(From="test@localhost", To=to)
    msg["Subject"] = Header(subject, "utf-8")
    msg.attach(MIMEText(body))
    path = os.path.join(context.attachment_dir, filename)
    with open(path, "rb") as fil:
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(fil.read())
        attachment.add_header(
            "Content-Disposition", "attachment", filename=os.path.basename(filename)
        )
        msg.attach(attachment)

    s = smtplib.SMTP("localhost", 8025)
    s.sendmail("test@localhost", [to], msg.as_string())
    s.quit()


@when('I send an email to "{to}" with subject "{subject}" and body "{body}"')
@persona_vars
def send_email(context, to, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = Header(subject, "utf-8")
    s = smtplib.SMTP("localhost", 8025)
    s.sendmail("test@localhost", [to], msg.as_string())
    s.quit()


@then('I should not have received any emails at "{address}"')
@persona_vars
def should_receive_no_messages(context, address):
    assert (
        context.mail.messages_for_user(address) == []
    ), f"Messages have been received at {address}"


@when("I clear the email messages")
@persona_vars
def clear_messages(context):
    context.mail.clear()
