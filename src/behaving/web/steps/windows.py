from behave import when


def remember_window(context, window, name):
    """ Associates a name to a Selenium WebDriver
    window handle to facilitate future lookup. """
    if not hasattr(context, "name_to_window_"):
        context.name_to_window_ = {}
    context.name_to_window_[name] = window


def lookup_window(context, name):
    """ Finds a Selenium WebDriver window handle by name """
    assert hasattr(context, "name_to_window_"), "No saved windows"
    assert name in context.name_to_window_, "{} not found in saved windows".format(name)
    return context.name_to_window_[name]


@when(u'I name the current window "{name}"')
def name_window(context, name):
    current = context.browser.driver.current_window_handle
    remember_window(context, current, name)


@when(u'I open a new window named "{name}" at "{url}"')
def open_window(context, name, url):
    driver = context.browser.driver
    driver.execute_script("window.open('{}', '{}')".format(url, name))
    new_window = driver.window_handles[-1]
    remember_window(context, new_window, name)
    # this is Selenium's way of switching windows
    driver.switch_to_window(new_window)


@when(u'I switch to the window named "{name}"')
def switch_window(context, name):
    """
    Changes the window Selenium executes subsequent commands on.

    Note: this doesn't bring the window to the front within
    the OS window manager.
    I tried executing "window.focus()", but that didn't work either.
    """
    window = lookup_window(context, name)
    context.browser.driver.switch_to_window(window)
