from behaving.sms.helpers import SMSChecker


def before_all(context):
    if not hasattr(context, 'sms_path'):
        context.sms_path = '/'
    context.sms = SMSChecker()
    context.sms.clear()


def before_feature(context, feature):
    pass


def before_scenario(context, scenario):
    context.users = dict()


def after_feature(context, feature):
    pass


def after_scenario(context, scenario):
    context.sms.clear()


def after_all(context):
    pass
