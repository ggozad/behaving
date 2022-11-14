from behave import then, when
from behaving.personas.persona import persona_vars
from behaving.web.steps.basic import _retry
from selenium.common.exceptions import NoAlertPresentException


@then(u"I should see an alert")
def alert_is_present(context):
    try:
        assert context.browser.get_alert(), u"Alert not found"
    except NoAlertPresentException:
        assert False, u"Alert not found"


@then(u"I should see an alert within {timeout:d} seconds")
def alert_is_present_timeout(context, timeout):
    def check():
        try:
            alert = context.browser.get_alert()
            return alert is not None
        except NoAlertPresentException:
            return False

    assert _retry(check, timeout), u"Alert not found"


@then(u'I should see an alert containing "{text}"')
def alert_contains_text(context, text):
    try:
        alert = context.browser.get_alert()
        assert text in alert.text, u"Text not found"
    except NoAlertPresentException:
        assert False, u"Alert not found"


@then(u'I should see an alert containing "{text}" within {timeout:d} seconds')
def alert_contains_text_timeout(context, text, timeout):
    def check():
        try:
            alert = context.browser.get_alert()
            return alert is not None and text in alert.text
        except NoAlertPresentException:
            return False

    assert _retry(check, timeout), u"Alert not found"


@when(u'I enter "{text}" to the alert')
@persona_vars
def set_alert_text(context, text):
    alert = context.browser.driver.switch_to.alert
    assert alert, u"Alert not found"
    alert.send_keys(text)


@when(u"I accept the alert")
def accept_alert(context):
    alert = context.browser.driver.switch_to.alert
    assert alert, u"Alert not found"
    alert.accept()


@when(u"I dismiss the alert")
def dimiss_alert(context):
    alert = context.browser.driver.switch_to.alert
    assert alert, u"Alert not found"
    alert.dismiss()
