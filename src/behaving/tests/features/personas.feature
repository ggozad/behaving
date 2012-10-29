Feature: Send an SMS

    @personas
    Scenario: Set variables
        Given "Foo" as the persona
        When I set "bar" to "Hello world"
        Then "bar" is set to "Hello world"
