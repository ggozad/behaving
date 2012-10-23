import os
from behaving.sms import environment as smsenv


def before_all(context):
    import behaving
    context.sms_path = os.path.join(os.path.dirname(behaving.__file__),
                                    '../../var/sms/')
    smsenv.before_all(context)


def after_all(context):
    smsenv.after_all(context)


def before_feature(context, feature):
    smsenv.before_feature(context, feature)


def after_feature(context, feature):
    smsenv.after_feature(context, feature)


def before_scenario(context, scenario):
    smsenv.before_scenario(context, scenario)


def after_scenario(context, scenario):
    smsenv.after_scenario(context, scenario)
