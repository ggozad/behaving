import os
from behaving.web import environment as webenv
from behaving.sms import environment as smsenv
from behaving.mail import environment as mailenv
from behaving.personas import environment as personaenv


def before_all(context):
    import behaving
    context.attachment_dir = os.path.join(os.path.dirname(behaving.__file__), 'tests/data')
    context.sms_path = os.path.join(os.path.dirname(behaving.__file__), '../../var/sms/')
    context.mail_path = os.path.join(os.path.dirname(behaving.__file__), '../../var/mail/')
    webenv.before_all(context)
    smsenv.before_all(context)
    mailenv.before_all(context)
    personaenv.before_all(context)


def after_all(context):
    webenv.after_all(context)
    smsenv.after_all(context)
    mailenv.after_all(context)
    personaenv.after_all(context)


def before_feature(context, feature):
    webenv.before_feature(context, feature)
    smsenv.before_feature(context, feature)
    mailenv.before_feature(context, feature)
    personaenv.before_feature(context, feature)


def after_feature(context, feature):
    webenv.after_feature(context, feature)
    smsenv.after_feature(context, feature)
    mailenv.after_feature(context, feature)
    personaenv.after_feature(context, feature)


def before_scenario(context, scenario):
    webenv.before_scenario(context, scenario)
    smsenv.before_scenario(context, scenario)
    mailenv.before_scenario(context, scenario)
    personaenv.before_scenario(context, scenario)


def after_scenario(context, scenario):
    webenv.after_scenario(context, scenario)
    smsenv.after_scenario(context, scenario)
    mailenv.after_scenario(context, scenario)
    personaenv.after_scenario(context, scenario)
