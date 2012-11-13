Feature: Grab contents of a DOM node, save it as a variable.


    @web
    Scenario: Detecting content. Setting variable.
        Given "Foo" as the persona
        When I visit "http://localhost:8080"
        Then I should see "Hello world"
        When I set "myvar" to the text of "helloworld"
        Then "myvar" is set to "Hello world!"
