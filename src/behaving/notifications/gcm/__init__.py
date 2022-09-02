import logging
import os

from behaving.fsinspector import FSInspector

logger = logging.getLogger("behaving")
# Generic setup/teardown for compatibility with pytest et al.


def setup(context):
    if not hasattr(context, "gcm_path"):
        path = os.path.join(os.getcwd(), "gcm")
        try:
            if not os.path.isdir(path):
                os.mkdir(path)
            logger.info(f"No default gcm path for gcmmock is specified. Using {path}")
        except OSError:
            logger.error(
                f"No default gcm path for gcmmock is specified. Unable to create {path}"
            )
            exit(1)
        context.gcm_path = path
    context.gcm = FSInspector(context.gcm_path)
    context.gcm.clear()
