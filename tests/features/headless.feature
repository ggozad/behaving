Feature: Headless browsers

    @web
    @headless
    Scenario: Text presence Chrome
        Given Chrome as the default browser
        Given a browser
        When I visit "http://web"
        Then I should see "Hello world"

    @web
    @headless
    Scenario: Text presence Firefox
        Given Firefox as the default browser
        Given a browser
        When I visit "http://web"
        Then I should see "Hello world"
