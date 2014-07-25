import os
from behaving import environment as benv


def before_all(context):
    import behaving
    context.attachment_dir = os.path.join(os.path.dirname(behaving.__file__), 'tests/data')
    context.sms_path = os.path.join(os.path.dirname(behaving.__file__), '../../var/sms/')
    context.mail_path = os.path.join(os.path.dirname(behaving.__file__), '../../var/mail/')
    context.screenshots_dir = os.path.join(os.path.dirname(behaving.__file__), '../../var/screenshots/')
    context.app_dir = os.path.join(os.path.dirname(behaving.__file__), 'tests/apps/')
    context.device_data_path = os.path.join(os.path.dirname(behaving.__file__), 'tests/apps/data')
    benv.before_all(context)


def after_all(context):
    benv.after_all(context)


def before_feature(context, feature):
    benv.before_feature(context, feature)


def after_feature(context, feature):
    benv.after_feature(context, feature)


def before_scenario(context, scenario):
    benv.before_scenario(context, scenario)


def after_scenario(context, scenario):
    benv.after_scenario(context, scenario)
