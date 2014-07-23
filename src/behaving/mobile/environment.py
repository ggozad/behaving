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
    if hasattr(context, 'device'):
        context.device.quit()
        del context.device


def after_all(context):
    teardown(context)
