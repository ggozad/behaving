import os
from behaving.web import environment as webenv
from behaving.sms import environment as smsenv


def before_all(context):
    import behaving
    context.attachment_dir = os.path.join(os.path.dirname(behaving.__file__), 'tests/data')
    context.sms_path = os.path.join(os.path.dirname(behaving.__file__),
                                    '../../var/sms/')
    webenv.before_all(context)
    smsenv.before_all(context)


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
