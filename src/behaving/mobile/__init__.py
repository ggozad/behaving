# Generic setup/teardown for compatibility with pytest et al.
def setup(context):
    if not hasattr(context, 'mobile_app_dir'):
        context.mobile_app_dir = '/'
    context.mobile_app_cache = {}
