import logging
import os

from behaving.fsinspector import FSInspector

logger = logging.getLogger("behaving")
# Generic setup/teardown for compatibility with pytest et al.


def setup(context):
    if not hasattr(context, "sms_path"):
        path = os.path.join(os.getcwd(), "sms")
        try:
            if not os.path.isdir(path):
                os.mkdir(path)
            logger.info(f"No default sms path for smsmock is specified. Using {path}")
        except OSError:
            logger.error(
                f"No default sms path for smsmock is specified. Unable to create {path}"
            )
            exit(1)
        context.sms_path = path
    context.sms = FSInspector(context.sms_path)
    context.sms.clear()
