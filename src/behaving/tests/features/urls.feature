Feature: Url handling

    Background:
        Given a browser

    @web
    Scenario: Visit a url
        When I visit "http://localhost:8080"
        Then the browser's URL should be "http://localhost:8080/"

    @web
    Scenario: Go to a url
        When I go to "http://localhost:8080/"
        Then the browser's URL should be "http://localhost:8080/"
        And the browser's URL should contain "localhost"
        And the browser's URL should not contain "google"
