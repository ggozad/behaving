import re


class Persona(dict):
    """
    A dictionary holding variables.
    """
    pass


var_exp = re.compile('\$(\w*)')


class PersonaVarMatcher(object):

    def __init__(self, func, *args):
        self.func = func

    def replace(self, *args, **kwargs):

        context = args[0]
        if hasattr(context, 'persona'):
            for kwname, kwvalue in kwargs.items():
                variables = var_exp.findall(str(kwvalue))
                for var in variables:
                    if var in context.persona:
                        kwargs[kwname] = kwargs[kwname].replace('$' + var, context.persona[var])

        self.func.__call__(*args, **kwargs)


def persona_vars(func):
    return PersonaVarMatcher(func).replace
