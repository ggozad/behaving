from . import setup, teardown


def before_all(context):
    setup(context)

    # Disable logging, selenium tends to be pretty verbose
    context.config.log_capture = False


def before_feature(context, feature):
    pass


def before_scenario(context, scenario):
    setup(context)


def after_feature(context, feature):
    pass


def after_scenario(context, scenario):
    teardown(context)


def after_all(context):
    teardown(context)
