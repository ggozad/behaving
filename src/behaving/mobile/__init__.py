# Generic setup/teardown for compatibility with pytest et al.
import logging

logger = logging.getLogger('behaving')


def setup(context):
    if not hasattr(context, 'webdriver_url'):
        context.webdriver_url = 'http://127.0.0.1:4723/wd/hub'
        logger.info('No default webdriver url is specified. Using %s' % context.webdriver_url)


def teardown(context):
    pass
