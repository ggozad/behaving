Feature: Text presence


    @web
    Scenario: Alert
        Given a browser
        When I visit "http://localhost:8080/alerts.html"
        And I press "alert"
            Then I should see an alert
        When I accept the alert
        And I press "alert-delayed"
            Then I should see an alert within 5 seconds
        When I accept the alert
        And I press "alert"
            Then I should see an alert containing "foo"
        When I accept the alert
        And I press "alert-delayed"
            Then I should see an alert containing "bar" within 5 seconds

    @web
    Scenario: Confirmations
        Given a browser
        When I visit "http://localhost:8080/alerts.html"
        And I press "confirm"
            Then I should see an alert
        When I accept the alert
            Then I should see "You are sure"
        When I press "confirm"
            Then I should see an alert
        When I dismiss the alert
            Then I should see "You are not sure"

    @web
    Scenario: Prompts
        Given a browser
        When I visit "http://localhost:8080/alerts.html"
        And I press "prompt"
            Then I should see an alert
        When I enter "foobar" to the alert
        And I accept the alert
            Then I should see "foobar"
