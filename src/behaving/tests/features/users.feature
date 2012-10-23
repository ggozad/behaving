Feature: Url handling

    @web
    Scenario: Change between users
        Given "Foo" as the user
        When I visit "http://localhost:8080"
        Then the browser's URL should be "http://localhost:8080/"
        Given "Bar" as the user
        When I visit "http://localhost:8080/page2.html"
        Then the browser's URL should be "http://localhost:8080/page2.html"
        Given "Foo" as the user
        Then the browser's URL should be "http://localhost:8080/"
