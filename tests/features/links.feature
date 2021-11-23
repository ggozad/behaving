Feature: Links

    Background:
        Given a browser

    @web
    Scenario: Clicking a link
        When I visit "http://web"
        And I click the link to "/page2.html"
        Then I should see "Page 2"
        When I visit "http://web"
        And I click the link to a url that contains "page2"
        Then I should see "Page 2"
        When I visit "http://web"
        And I click the link with text "Page 2"
        Then I should see "Page 2"
        When I visit "http://web"
        And I click the link with text that contains "age 2"
        Then I should see "Page 2"
