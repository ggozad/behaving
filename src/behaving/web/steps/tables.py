from behave import then

from behaving.personas.persona import persona_vars


def _process_table(table):
    headers = [el.text for el in table.find_by_tag("th")]
    # We should be using here rows = table.find_by_xpath("//tr[not(th)]")
    # but for some reason this duplicates the rows.
    rows = [r for r in table.find_by_tag("tr") if r.find_by_tag("td")]
    cells = [[cell.text for cell in row.find_by_tag("td")] for row in rows]
    return headers, cells


@then(u'the table with id "{id}" should be')
@persona_vars
def table_equals(context, id):
    try:
        table = context.browser.find_by_id(id).first
    except IndexError:
        assert False, u"Table not found"

    headers, cells = _process_table(table)
    if headers:
        assert headers == context.table.headings, u"Table headers do not match"

    assert [
        [cell for cell in row] for row in context.table.rows
    ] == cells, "Table cells do not match"
