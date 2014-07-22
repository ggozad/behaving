from . import setup, teardown


def before_all(context):
    setup(context)


def before_feature(context, feature):
    pass


def before_scenario(context, scenario):
    pass


def after_feature(context, feature):
    pass


def after_scenario(context, scenario):
    if hasattr(context, 'mobile'):
        context.mobile.quit()
        del context.mobile


def after_all(context):
    teardown(context)
