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

    @web
    Scenario: Base url
        Given the base url "http://localhost:8080/"
        When I go to "/page2.html"
        Then the browser's URL should be "http://localhost:8080/page2.html"
        And the browser's URL should be "/page2.html"
        And the browser's URL should contain "localhost"

    @web
    Scenario: Parse a url
    Given "Foo" as the persona
    Given the base url "http://localhost:8080/"
        When I go to "/page2.html"
        And I parse the url path and set "/page{page_no}.html"
        Then "page_no" is set to "2"