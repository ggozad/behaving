import re


class Persona(dict):
    """
    A dictionary holding variables.
    """
    def get_value(self, path):
        current = self
        components = path.split(".")
        for component in components:
            if hasattr(current, component):
                current = getattr(current, component)
            else:
                current = current[component]
        return current

    def set_value(self, path, value):
        current = self
        components = path.split(".")
        prop = components.pop()
        for component in components:
            if hasattr(current, component):
                current = getattr(current, component)
            else:
                try:
                    current = current[component]
                except KeyError, e:
                    current[component] = {}
                    current = current[component]
        
        if isinstance(current, dict):
            current[prop] = value
        else:
            setattr(current, prop, value)


var_exp = re.compile('\$(\w+(?:\.\w+)*)')


class PersonaVarMatcher(object):

    def __init__(self, func, *args):
        self.func = func

    def replace(self, *args, **kwargs):
        context = args[0]
        if hasattr(context, 'persona'):
            for kwname, kwvalue in kwargs.items():
                variables = var_exp.findall(str(kwvalue))
                for var in variables:
                    value = context.persona.get_value(var)
                    kwargs[kwname] = kwargs[kwname].replace('$' + var, value)

        self.func.__call__(*args, **kwargs)


def persona_vars(func):
    return PersonaVarMatcher(func).replace
