import os                                                                       
from behave import step                                                         
from behaving.personas.persona import persona_vars           


@step(u'I note browser session')
def record_browser_session(context):
    if hasattr(context, 'current_sessions'):
        current_sessions = context.current_sessions
    else:
        current_sessions = set()
    current_sessions.add(context.browser.driver)
    context.current_sessions = current_sessions

@step(u'I only used one browser session')
def only_used_one_browser_session(context):
    sessions = len(context.current_sessions)
    assert sessions  == 1, 'Oops, I used %s browsers sessions!' % sessions

