import logging
import os

from behaving.fsinspector import FSInspector

logger = logging.getLogger('behaving')


def before_all(context):
    if not hasattr(context, 'sms_path'):
        path = os.path.join(os.getcwd(), 'sms')
        try:
            if not os.path.isdir(path):
                os.mkdir(path)
            logger.info('No default sms path for smsmock is specified. Using %s' % path)
        except OSError:
            logger.error('No default sms path for smsmock is specified. Unable to create %s' % path)
            exit(1)
        context.sms_path = path
    context.sms = FSInspector(context.sms_path)
    context.sms.clear()


def before_feature(context, feature):
    pass


def before_scenario(context, scenario):
    pass


def after_feature(context, feature):
    pass


def after_scenario(context, scenario):
    context.sms.clear()


def after_all(context):
    pass
