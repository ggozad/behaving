import re
import sys

# unicode and basestring was removed from Python 3
is_python3 = sys.version_info.major == 3
if is_python3:
    unicode = str
    basestring = str


class Persona(dict):
    """
    A dictionary holding variables.
    """

    pass


var_exp = re.compile(r"(?<!\\)\$(\w+(?:\.\w+)*)")


class PersonaVarMatcher(object):
    def __init__(self, func, *args):
        self.func = func

    def _get_variables(self, target):
        if isinstance(target, unicode):
            target = target.encode("utf-8")
        return var_exp.findall(str(target))

    def _replace_variables(self, context, target):
        for var in self._get_variables(target):
            value = context.persona[var]

            if isinstance(value, basestring):
                target = target.replace("$" + var, value)
            else:
                target = value
        if isinstance(target, basestring):
            target = target.replace("\\$", "$")

        return target

    def replace(self, *args, **kwargs):
        context = args[0]
        if hasattr(context, "persona"):
            for kwname, kwvalue in kwargs.items():
                kwargs[kwname] = self._replace_variables(context, kwargs[kwname])
            if hasattr(context, "text") and context.text:
                context.text = self._replace_variables(context, context.text)

        self.func.__call__(*args, **kwargs)


def persona_vars(func):
    return PersonaVarMatcher(func).replace
