from behaving.fsinspector import FSInspector


def before_all(context):
    if not hasattr(context, 'mail_path'):
        context.mail_path = '/'
    context.mail = FSInspector(context.mail_path)
    context.mail.clear()


def before_feature(context, feature):
    pass


def before_scenario(context, scenario):
    context.users = dict()


def after_feature(context, feature):
    pass


def after_scenario(context, scenario):
    context.mail.clear()


def after_all(context):
    pass
