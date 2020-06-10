# Generic setup/teardown for compatibility with pytest et al.
from .ios import *
from .android import *


def setup(context):
    if not hasattr(context, "mobile_app_dir"):
        context.mobile_app_dir = "/"
