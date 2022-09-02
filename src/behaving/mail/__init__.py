import logging
import os

from behaving.fsinspector import FSInspector

logger = logging.getLogger("behaving")

# Generic setup/teardown for compatibility with pytest et al.


def setup(context):
    if not hasattr(context, "mail_path"):
        path = os.path.join(os.getcwd(), "mail")
        try:
            if not os.path.isdir(path):
                os.mkdir(path)
            logger.info(f"No default mail path for mailmock is specified. Using {path}")
        except OSError:
            logger.error(f"No default mail path for mailmock is specified. Unable to create {path}")
            exit(1)
        context.mail_path = path
    context.mail = FSInspector(context.mail_path)
    context.mail.clear()
