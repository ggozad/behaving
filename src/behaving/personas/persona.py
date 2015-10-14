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

var_exp = re.compile(r'(?<!\\)\$(\w+(?:\.\w+)*)')


class PersonaVarMatcher(object):

    def __init__(self, func, *args):
        self.func = func

    def replace_one(self, context, target_value):
        if isinstance(target_value, unicode):
            target_value = target_value.encode('utf-8')
        variables = var_exp.findall(str(target_value))
        for var in variables:
            value = context.persona[var]

            if isinstance(value, basestring):
                target_value = target_value.replace('$' + var, value)
            else:
                target_value = value
        if isinstance(target_value, basestring):
            target_value = target_value.replace('\$', '$')

        return target_value

    def replace(self, *args, **kwargs):
        context = args[0]
        if hasattr(context, 'persona'):
            for kwname, kwvalue in kwargs.items():
                kwargs[kwname] = self.replace_one(context, kwargs[kwname])
            if hasattr(context, 'text') and context.text:
                context.text = self.replace_one(context, context.text)

        self.func.__call__(*args, **kwargs)


def persona_vars(func):
    return PersonaVarMatcher(func).replace
