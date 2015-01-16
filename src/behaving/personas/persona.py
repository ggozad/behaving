import re


class Persona(dict):
    """
    A dictionary holding variables.
    """
    pass

var_exp = re.compile(r'(?<!\\)\$(\w+(?:\.\w+)*)')


class PersonaVarMatcher(object):

    def __init__(self, func, *args):
        self.func = func

    def replace(self, *args, **kwargs):
        context = args[0]
        if hasattr(context, 'persona'):
            for kwname, kwvalue in kwargs.items():
                if isinstance(kwvalue, unicode):
                    kwvalue = kwvalue.encode('utf-8')
                variables = var_exp.findall(str(kwvalue))
                for var in variables:
                    value = context.persona[var]

                    if isinstance(value, basestring):
                        kwargs[kwname] = kwargs[kwname].replace('$' + var, value)
                    else:
                        kwargs[kwname] = value
                if isinstance(kwargs[kwname], basestring):
                    kwargs[kwname] = kwargs[kwname].replace('\$', '$')

        self.func.__call__(*args, **kwargs)


def persona_vars(func):
    return PersonaVarMatcher(func).replace
