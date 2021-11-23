Feature: Text presence

    @web
    @headless
    Scenario: Text presence
        Given Chrome as the default browser
        Given a browser
        When I visit "http://web"
        Then I should see "Hello world"

    @web
    @headless
    Scenario: Text presence
        Given Firefox as the default browser
        Given a browser
        When I visit "http://web"
        Then I should see "Hello world"
