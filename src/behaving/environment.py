from behaving.web import environment as webenv
from behaving.sms import environment as smsenv
from behaving.mail import environment as mailenv
from behaving.personas import environment as personaenv
from behaving.mobile import environment as mobileenv


def before_all(context):
    webenv.before_all(context)
    smsenv.before_all(context)
    mailenv.before_all(context)
    mobileenv.before_all(context)
    personaenv.before_all(context)
    context.config.log_capture = False


def after_all(context):
    webenv.after_all(context)
    smsenv.after_all(context)
    mailenv.after_all(context)
    mobileenv.after_all(context)
    personaenv.after_all(context)


def before_feature(context, feature):
    webenv.before_feature(context, feature)
    smsenv.before_feature(context, feature)
    mailenv.before_feature(context, feature)
    mobileenv.before_feature(context, feature)
    personaenv.before_feature(context, feature)


def after_feature(context, feature):
    webenv.after_feature(context, feature)
    smsenv.after_feature(context, feature)
    mobileenv.after_feature(context, feature)
    mailenv.after_feature(context, feature)
    personaenv.after_feature(context, feature)


def before_scenario(context, scenario):
    webenv.before_scenario(context, scenario)
    smsenv.before_scenario(context, scenario)
    mailenv.before_scenario(context, scenario)
    mobileenv.before_scenario(context, scenario)
    personaenv.before_scenario(context, scenario)


def after_scenario(context, scenario):
    webenv.after_scenario(context, scenario)
    smsenv.after_scenario(context, scenario)
    mailenv.after_scenario(context, scenario)
    mobileenv.after_scenario(context, scenario)
    personaenv.after_scenario(context, scenario)
