Feature: HTML tables

    Background:
        Given a browser

    @web
    Scenario: Asserting the contents of a table
        When I visit "http://web/tables.html"
        Then the table with id "customers-thead" should be
            | Company                    | Contact         | Country   |
            | Alfreds Futterkiste        | Maria Anders    | Germany   |
            | Centro comercial Moctezuma | Francisco Chang | Mexico    |
            | Ernst Handel               | Roland Mendel   | Austria   |

        And the table with id "customers-headers" should be
            | Company                    | Contact         | Country   |
            | Alfreds Futterkiste        | Maria Anders    | Germany   |
            | Centro comercial Moctezuma | Francisco Chang | Mexico    |
            | Ernst Handel               | Roland Mendel   | Austria   |

        And the table with id "customers-no-headers" should be
            |                            |                 |           |
            | Alfreds Futterkiste        | Maria Anders    | Germany   |
            | Centro comercial Moctezuma | Francisco Chang | Mexico    |
            | Ernst Handel               | Roland Mendel   | Austria   |

    @web
    Scenario: Asserting table does/(does not) contain rows
        When I visit "http://web/tables.html"
        Then the table with id "customers-thead" should contain the rows
            | Alfreds Futterkiste        | Maria Anders    | Germany   |
            | Ernst Handel               | Roland Mendel   | Austria   |

        And the table with id "customers-thead" should not contain the rows
            | foo                        | Maria Anders    | Germany   |
            | Ernst Handel               | bar             | Austria   |
