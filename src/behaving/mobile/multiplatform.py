import sys


class MultiplatformException(Exception):
    pass


class Multiplatform(object):
    """
    Decorate steps that work differently depending on the
    platform (Browser, iOS, Android) using this function.
    The step is then expected to define the appropriate local functions
    and not assert anything itself. The decorator will then find the appropriate
    local and use that.
    """

    def __init__(self, func, *args):
        self.func = func
        self._locals = {}

    def platform_specific(self, context, *args, **kwargs):

        def tracer(frame, event, arg):
            if event == 'return':
                self._locals = frame.f_locals.copy()

        # tracer is activated on next call, return or exception
        sys.setprofile(tracer)
        try:
            # trace the function call
            self.func(context, *args, **kwargs)
        finally:
            # disable tracer and replace with old one
            sys.setprofile(None)

        if hasattr(context, 'browser') and 'browser' in self._locals:
            return self._locals['browser'](context, *args, **kwargs)
        elif hasattr(context, 'device'):
            if context.device.capabilities['platformName'] == 'iOS' and 'ios' in self._locals:
                return self._locals['ios'](context, *args, **kwargs)
            elif context.device.capabilities['platformName'] == 'Android' and 'android' in self._locals:
                return self._locals['android'](context, *args, **kwargs)
            elif 'mobile' in self._locals:
                return self._locals['mobile'](context, *args, **kwargs)

        raise MultiplatformException(
            "Function %s was decorated with @multiplatform but could not find appropriate context" % self.func)


def multiplatform(func):
    return Multiplatform(func).platform_specific
