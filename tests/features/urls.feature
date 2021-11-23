Feature: Url handling

    @web
    Scenario: Visit a url
        Given a browser
        When I visit "http://web"
        Then the browser's URL should be "http://web/"

    @web
    Scenario: Go to a url
        Given a browser
        When I go to "http://web/"
        Then the browser's URL should be "http://web/"
        And the browser's URL should contain "localhost"
        And the browser's URL should not contain "google"

    @web
    Scenario: Base url
        Given a browser
        Given the base url "http://web/"
        When I go to "/page2.html"
        Then the browser's URL should be "http://web/page2.html"
        And the browser's URL should be "/page2.html"
        And the browser's URL should contain "localhost"

    @web
    Scenario: Parse a url
        Given "Foo" as the persona
        Given the base url "http://web/"
        When I go to "/page2.html"
        And I parse the url path and set "/page{page_no}.html"
        Then "page_no" is set to "2"