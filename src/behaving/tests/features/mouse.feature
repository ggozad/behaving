Feature: Mouse interactions

    @web
    Scenario: Mouse over and out
        Given a browser
        When I visit "http://localhost:8080/mouse.html"
        And I mouse over the element with xpath "//span[@id='mouse-interaction']"
            Then I should see "Over"
        When I mouse out of the element with xpath "//span[@id='mouse-interaction']"
            Then I should see "and out"