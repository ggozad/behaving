from behave import step


@step(u"I enable single browser mode")
def enable_single_browser_mode(context):
    context.single_browser = True


@step(u"I note browser session")
def record_browser_session(context):
    if hasattr(context, "current_sessions"):
        current_sessions = context.current_sessions
    else:
        current_sessions = set()
    current_sessions.add(context.browser.driver)
    context.current_sessions = current_sessions


@step(u"I only used one browser session")
def only_used_one_browser_session(context):
    sessions = len(context.current_sessions)
    assert sessions == 1, "Oops, I used %s browsers sessions!" % sessions


@step(u"I pause the tests")
def pause_tests(context):
    context._runner.stop_capture()
    print("\tPress ENTER to continue")
    try:
        input()
    except SyntaxError:
        pass
    context._runner.start_capture()
