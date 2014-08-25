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
                if type(current) == type(self.get_value):
                    current = current()
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
                except KeyError:
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

                    if type(value) == str or type(value) == unicode:
                        kwargs[kwname] = kwargs[kwname].replace('$' + var, value)
                    else:
                        kwargs[kwname] = value

        self.func.__call__(*args, **kwargs)


def persona_vars(func):
    return PersonaVarMatcher(func).replace
