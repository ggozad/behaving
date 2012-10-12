import os
from behaving.web import environment as webenv


def before_all(context):
    webenv.before_all(context)
    import behaving.web.tests
    context.attachment_dir = os.path.join(os.path.dirname(behaving.web.tests.__file__), 'data')


def after_all(context):
    webenv.after_all(context)


def before_feature(context, feature):
    webenv.before_feature(context, feature)


def after_feature(context, feature):
    webenv.after_feature(context, feature)


def before_scenario(context, scenario):
    webenv.before_scenario(context, scenario)


def after_scenario(context, scenario):
    webenv.after_scenario(context, scenario)
