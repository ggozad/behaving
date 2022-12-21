Feature: HTML tables

    Background:
        Given a browser

    @web
    Scenario: Asserting the contents of a table
        When I visit "http://web/tables.html"
        Then the table with id "customers-thead" should be
            | Company                    | Contact         | Country |
            | Alfreds Futterkiste        | Maria Anders    | Germany |
            | Centro comercial Moctezuma | Francisco Chang | Mexico  |
            | Ernst Handel               | Roland Mendel   | Austria |

        And the table with id "customers-headers" should be
            | Company                    | Contact         | Country |
            | Alfreds Futterkiste        | Maria Anders    | Germany |
            | Centro comercial Moctezuma | Francisco Chang | Mexico  |
            | Ernst Handel               | Roland Mendel   | Austria |

        And the table with id "customers-no-headers" should be
            |                            |                 |         |
            | Alfreds Futterkiste        | Maria Anders    | Germany |
            | Centro comercial Moctezuma | Francisco Chang | Mexico  |
            | Ernst Handel               | Roland Mendel   | Austria |

        Then the table with xpath "//table[@id='customers-thead']" should be
            | Company                    | Contact         | Country |
            | Alfreds Futterkiste        | Maria Anders    | Germany |
            | Centro comercial Moctezuma | Francisco Chang | Mexico  |
            | Ernst Handel               | Roland Mendel   | Austria |

    @web
    Scenario: Asserting table does/(does not) contain rows
        When I visit "http://web/tables.html"
        Then the table with id "customers-thead" should contain the rows
            | Alfreds Futterkiste | Maria Anders  | Germany |
            | Ernst Handel        | Roland Mendel | Austria |

        And the table with xpath "//table[@id='customers-thead']" should contain the rows
            | Alfreds Futterkiste | Maria Anders  | Germany |
            | Ernst Handel        | Roland Mendel | Austria |

        And the table with id "customers-no-headers" should not contain the rows
            | foo          | Maria Anders | Germany |
            | Ernst Handel | bar          | Austria |

        And the table with xpath "//table[@id='customers-thead']" should not contain the rows
            | foo          | Maria Anders | Germany |
            | Ernst Handel | bar          | Austria |

    @web
    Scenario: Asserting equality on specific rows
        When I visit "http://web/tables.html"
        Then row 0 in the table with id "customers-thead" should be
            | Alfreds Futterkiste | Maria Anders | Germany |
        And row 1 in the table with id "customers-thead" should be
            | Centro comercial Moctezuma | Francisco Chang | Mexico |
        And row 2 in the table with xpath "//table[@id='customers-thead']" should be
            | Ernst Handel | Roland Mendel | Austria |

    @web
    Scenario: Asserting equality on specific cells
        When I visit "http://web/tables.html"
        Then the value of the cell in row 0, column 2 in the table with id "customers-thead" should be "Germany"
        And the value of the cell in row 0, column 2 in the table with xpath "//table[@id='customers-thead']" should be "Germany"
        And the value of the cell in row 0, column "Country" in the table with id "customers-thead" should be "Germany"
        And the value of the cell in row 0, column "Country" in the table with xpath "//table[@id='customers-thead']" should be "Germany"
