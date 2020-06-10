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

    assert res, u"expression not found"
    assert res.named, u"expression not found"
    for key, val in res.named.items():
        context.persona[key] = val
