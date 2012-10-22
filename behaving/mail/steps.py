import time
import re
from behave import when, then

MAIL_TIMEOUT = 5
URL_RE = re.compile(r'((?:ftp|https?)://(localhost|([12]?[0-9]{1,2}.){3}([12]?[0-9]{1,2})|(?:[a-z0-9](?:[-a-z0-9]*[a-z0-9])?\.)+(?:com|edu|biz|org|gov|int|info|mil|net|name|museum|coop|aero|[a-z][a-z]))\b(?::\d+)?(?:\/[^"\'<>()\[\]{}\s\x7f-\xff]*(?:[.,?]+[^"\'<>()\[\]{}\s\x7f-\xff]+)*)?)', re.I|re.S|re.U)


def filter_emails(context, address, f=None):
    emails = []
    start = time.time()
    while time.time() - start < MAIL_TIMEOUT:
        emails = filter(f, context.mail.mail_for_user(address))
        if emails:
            break
        time.sleep(0.2)
    return emails


@then('I should receive an email at "{address}" containing "{text}"')
def should_receive_email_containing_text(context, address, text):

    def filter_contents(mail):
        return text in mail.get_payload()

    assert filter_emails(context, address, filter_contents)


@then('I should receive an email at "{address}" with subject "{subject}"')
def should_receive_email_with_subject(context, address, subject):

    def filter_contents(mail):
        return subject == mail.get('Subject')

    assert filter_emails(context, address, filter_contents)


@then('I should receive an email at "{address}"')
def should_receive_email(context, address):
    assert filter_emails(context, address)


@when('I click the link in the email I received at "{email}"')
def click_link_in_email(context, email):
    emails = filter_emails(context, email)
    assert emails
    email = emails[0]
    links = URL_RE.findall(email.get_payload().replace('=\n', ''))
    assert links
    url = links[0][0]
    context.browser.visit(url)
