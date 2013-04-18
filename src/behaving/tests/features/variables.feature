Feature: Grab contents of a DOM node, save it as a variable.


    @web
    Scenario: Setting variable to the text of a node
        Given "Foo" as the persona
        When I visit "http://localhost:8080"
        Then I should see "Hello world"
        When I set "myvar" to the text of "helloworld"
        Then "myvar" is set to "Hello world!"

    @web
    Scenario: Setting variable to an attribute of an xpath selection
        Given "Foo" as the persona
        When I visit "http://localhost:8080"
        And I set "myvar" to the attribute "data-test" of the element with xpath "//div[@id='xpath-id']"
        Then "myvar" is set to "testing"
