from pprint import pformat

from behave import then
from splinter.exceptions import ElementDoesNotExist

from behaving.personas.persona import persona_vars


def _process_table(table):

    headers = [el.text for el in table.find_by_tag("th")]
    # We should be using here rows = table.find_by_xpath("//tr[not(th)]")
    # but for some reason this duplicates the rows.
    rows = [r for r in table.find_by_tag("tr") if r.find_by_tag("td", wait_time=0)]
    cells = [[cell.text for cell in row.find_by_tag("td")] for row in rows]
    return headers, cells


def _find_table_by_id_or_xpath(context, selector):
    try:
        table = context.browser.find_by_id(selector) or context.browser.find_by_xpath(
            selector
        )
        return table.first
    except (
        IndexError,
        ElementDoesNotExist,
    ):
        assert False, f"Table with id or xpath {selector} not found"


@then('the table with id "{selector}" should be')
@then('the table with xpath "{selector}" should be')
@persona_vars
def table_equals(context, selector):
    table = _find_table_by_id_or_xpath(context, selector)
    headers, cells = _process_table(table)
    if headers:
        assert headers == context.table.headings, (
            f"Table headers do not match. Expected:\n"
            f"{context.table.headings}\n"
            f"Got:\n"
            f"{headers}"
        )
    expected_cells = [[cell for cell in row] for row in context.table.rows]
    assert expected_cells == cells, (
        f"Table cells do not match. Expected:\n"
        f"{pformat(expected_cells)}\n"
        f"Got:\n"
        f"{pformat(cells)}"
    )


@then('the table with id "{selector}" should contain the rows')
@then('the table with xpath "{selector}" should contain the rows')
@persona_vars
def table_contains(context, selector):
    table = _find_table_by_id_or_xpath(context, selector)
    _, cells = _process_table(table)
    for row in [*context.table.rows, context.table.headings]:
        assert [cell for cell in row] in cells, f"{row} not found"


@then('the table with id "{selector}" should not contain the rows')
@then('the table with xpath "{selector}" should not contain the rows')
@persona_vars
def table_does_not_contain(context, selector):
    table = _find_table_by_id_or_xpath(context, selector)
    _, cells = _process_table(table)
    for row in [*context.table.rows, context.table.headings]:

        assert [cell for cell in row] not in cells, f"{row} found"


@then('row {row_no:d} in the table with id "{selector}" should be')
@then('row {row_no:d} in the table with xpath "{selector}" should be')
@persona_vars
def row_equals(context, row_no, selector):
    table = _find_table_by_id_or_xpath(context, selector)

    _, cells = _process_table(table)
    expected_row = [cell for cell in context.table.headings]
    assert expected_row == cells[row_no], (
        f"Rows did not match. Expected:\n"
        f"{expected_row}\n"
        f"Got:\n"
        f"{cells[row_no]}"
    )


@then(
    'the value of the cell in row {row_no:d}, column {col_no:d} in the table with id "{selector}" should be "{value}"'
)
@then(
    'the value of the cell in row {row_no:d}, column {col_no:d} in the table with xpath "{selector}" should be "{value}"'
)
@persona_vars
def cell_equals(context, row_no, col_no, selector, value):
    table = _find_table_by_id_or_xpath(context, selector)

    _, cells = _process_table(table)
    assert (
        cells[row_no][col_no] == value
    ), f"Cells do not match, expected {value} but got {cells[row_no][col_no]}"


@then(
    'the value of the cell in row {row_no:d}, column "{col_header}" in the table with id "{selector}" should be "{value}"'
)
@then(
    'the value of the cell in row {row_no:d}, column "{col_header}" in the table with xpath "{selector}" should be "{value}"'
)
@persona_vars
def cell_equals_with_column_header(context, row_no, col_header, selector, value):
    table = _find_table_by_id_or_xpath(context, selector)

    headers, cells = _process_table(table)
    assert (
        cells[row_no][headers.index(col_header)] == value
    ), f"Cells do not match, expected {value} but got {cells[row_no][headers.index(col_header)]}"
