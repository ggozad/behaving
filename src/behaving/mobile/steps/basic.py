import os

from behave import step
from ..ios import IOSWebDriver

@step(u'I should see an element with accessibility id "{id}"')
def see_accessibility_id(context, id):
    assert context.browser.find_by_accessibility_id(id)
