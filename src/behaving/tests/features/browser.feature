Feature: Browser handling

    @web
    Scenario: Select Chrome browser
        Given Chrome as the default browser
        Given a browser

    @web
    Scenario: Select Firefox browser
        Given Firefox as the default browser
        Given a browser

    @web
    Scenario: Select PhantomJS browser
        Given PhantomJS as the default browser
        Given a browser

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

    @web
    Scenario: Change between named browsers
        Given browser "Foo"
        When I visit "http://localhost:8080"
        Then the browser's URL should be "http://localhost:8080/"
        Given browser "Bar"
        When I visit "http://localhost:8080/page2.html"
        Then the browser's URL should be "http://localhost:8080/page2.html"
        Given browser "Foo"
        Then the browser's URL should be "http://localhost:8080/"

    @web
    Scenario: Browser cookies
        Given a browser
        Given "Foo" as the persona
        When I visit "http://localhost:8080"
        And I set the cookie "foo" to "bar"
        And I evaluate the script "document.cookie" and assign the result to "cookie"
        Then "cookie" is set to "foo=bar"
        When I set the cookie "bar" to "foo"
        And I evaluate the script "document.cookie" and assign the result to "cookie"
        Then "cookie" is set to "foo=bar; bar=foo"
        When I delete the cookie "foo"
        And I evaluate the script "document.cookie" and assign the result to "cookie"
        Then "cookie" is set to "bar=foo"
        When I delete all cookies
        And I evaluate the script "document.cookie || 'none'" and assign the result to "cookie"
        Then "cookie" is set to "none"

    @web
    Scenario: Change browser size
        Given a browser
        When I visit "http://localhost:8080"
        And I resize the browser to 800x600
        Then I should see "Hidden in mobile"
        When I resize the browser to 300x200
        Then I should not see "Hidden in mobile"

    @web
    Scenario: Change viewport size
        Given a browser
        When I visit "http://localhost:8080"
        And I resize the viewport to 501x800
        Then I should see "Hidden in mobile"
        When I resize the viewport to 499x800
        Then I should not see "Hidden in mobile"
