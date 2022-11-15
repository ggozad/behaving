import warnings

import parse


def parse_text(context, text, expression):
    parser = parse.compile(expression)
    res = parser.parse(text)

    # Make an implicit assumption that there might be something before the expression
    if res is None:
        expr = "{}" + expression
        parser = parse.compile(expr)
        res = parser.parse(text)

    # Make an implicit assumption that there might be something after the expression
    if res is None:
        expr = expression + "{}"
        parser = parse.compile(expr)
        res = parser.parse(text)

    # Make an implicit assumption that there might be something before/after the expression
    if res is None:
        expr = "{}" + expression + "{}"
        parser = parse.compile(expr)
        res = parser.parse(text)

    assert res, "expression not found"
    assert res.named, "expression not found"
    for key, val in res.named.items():
        context.persona[key] = val


def deprecated(from_step, to_step):
    def inner_deprecated(func):
        def wrapped(*args, **kwargs):
            context = args[0]
            def log():
                warnings.simplefilter('always', DeprecationWarning)  # turn off filter
                warnings.warn(f'Call to deprecated step. Use:\n "{to_step}" \ninstead of:\n"{from_step}"\n', category=DeprecationWarning)
                warnings.simplefilter('default', DeprecationWarning)  # reset filter
            context.add_cleanup(log)
            return func(*args, **kwargs)
        return wrapped
    return inner_deprecated