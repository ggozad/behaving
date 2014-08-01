import re


class Persona(dict):
    """
    A dictionary holding variables.
    """
    pass


var_exp = re.compile('\$(\w+(?:\.\w+)*)')


class PersonaVarMatcher(object):

    def __init__(self, func, *args):
        self.func = func

    def replace(self, *args, **kwargs):
        import pdb
        context = args[0]
        if hasattr(context, 'persona'):
            for kwname, kwvalue in kwargs.items():
                variables = var_exp.findall(str(kwvalue))
                for var in variables:
                    components = var.split(".")
                    current = context.persona
                    for component in components:
                        if hasattr(current, component):
                            current = getattr(current, component)
                        else:
                            current = current[component]

                    if current != context.persona:
                        kwargs[kwname] = kwargs[kwname].replace('$' + var, current)

        self.func.__call__(*args, **kwargs)


def persona_vars(func):
    return PersonaVarMatcher(func).replace
