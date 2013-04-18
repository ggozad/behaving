Feature: Send an SMS

    @personas
    Scenario: Get/Set variables
        Given "Foo" as the persona
        When I set "bar" to "Hello world"
        Then "bar" is set to "Hello world"

    @personas
    Scenario: Parse variables in steps
        Given "Foo" as the persona
        When I set "foo" to "Hello world"
        And I set "bar" to "Hello world"
        Then "foo" is set to "$bar"
        When I set "foo" to "world"
        And I set "bar" to "Hello $foo"
        Then "bar" is set to "Hello world"