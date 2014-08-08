class Multiplatform(object):

    def __init__(self, func, *args):
        self.func = func
        self.browser = None
        self.iOS = None

    def platform_specific(self, context, *args, **kwargs):
        if hasattr(context, 'browser'):
            platform = 'browser'
        elif hasattr(context, 'device'):
            platform = 'ios'

        return self.func.__call__(context, *args, **kwargs)[platform](context, *args, **kwargs)

    def browser(*args, **kwargs):
        pass


def multiplatform(func):
    return Multiplatform(func).platform_specific
