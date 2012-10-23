Feature: Browser handling

    @web
    Scenario: Select Chrome browser
        Given Chrome as the browser

    @web
    Scenario: Select Firefox browser
        Given Firefox as the browser

    @web
    Scenario: History
        Given a browser
        When I visit "http://localhost:8080"
        And I visit "http://localhost:8080/page2.html"
        Then the browser's URL should be "http://localhost:8080/page2.html"
        When I go back
        Then the browser's URL should be "http://localhost:8080/"
        When I go forward
        Then the browser's URL should be "http://localhost:8080/page2.html"
