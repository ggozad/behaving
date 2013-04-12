import email
import re
from behave import step
from behaving.personas.persona import persona_vars


MAIL_TIMEOUT = 5
URL_RE = re.compile(r'((?:ftp|https?)://(localhost|([12]?[0-9]{1,2}.){3}([12]?[0-9]{1,2})|(?:[a-z0-9](?:[-a-z0-9]*[a-z0-9])?\.)+(?:com|edu|biz|org|gov|int|info|mil|net|name|museum|coop|aero|[a-z][a-z]))\b(?::\d+)?(?:\/[^"\'<>()\[\]{}\s\x7f-\xff]*(?:[.,?]+[^"\'<>()\[\]{}\s\x7f-\xff]+)*)?)', re.I|re.S|re.U)


@step(u'I should receive an email at "{address}" containing "{text}"')
@persona_vars
def should_receive_email_containing_text(context, address, text):

    def filter_contents(mail):
        mail = email.message_from_string(mail)
        return text in mail.get_payload()

    assert context.mail.user_messages(address, filter_contents)


@step(u'I should receive an email at "{address}" with subject "{subject}"')
@persona_vars
def should_receive_email_with_subject(context, address, subject):

    def filter_contents(mail):
        mail = email.message_from_string(mail)
        return subject == mail.get('Subject')

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
    mail = email.message_from_string(mails[0])
    links = URL_RE.findall(mail.get_payload().replace('=\n', ''))
    assert links, u'link not found'
    url = links[0][0]
    context.browser.visit(url)
