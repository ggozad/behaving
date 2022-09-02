Feature: Mouse interactions

    @web
    Scenario: Mouse over and out
        # Firefox has trouble with mouse-out
        Given Chrome as the default browser
        Given a browser
        When I visit "http://web/mouse.html"
        And I mouse over the element with xpath "//span[@id='mouse-interaction']"
        Then I should see "Over"
        When I mouse out of the element with xpath "//span[@id='mouse-interaction']"
        Then I should see "and out"