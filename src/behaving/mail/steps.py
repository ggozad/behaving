import email
import re
import quopri
from behave import step
from behaving.personas.persona import persona_vars


MAIL_TIMEOUT = 5
URL_RE = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                    re.I | re.S | re.U)


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
    def filter_contents(mail):
        mail = email.message_from_string(mail)
        return subject == mail.get('Subject')

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
