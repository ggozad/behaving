Feature: Use Personas

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

    @personas
        Scenario: Don't start up multiple browsers
        Given I enable single browser mode
        And browser "Chrome"
        And I note browser session
        When I visit "http://localhost:8080"
        And I note browser session
        Given "Foo" as the persona
        And I note browser session
        When I visit "http://localhost:8080"
        And I note browser session
        And I set "bar" to "Hello world"
        Then "bar" is set to "Hello world"
        Given "Bar" as the persona
        And I note browser session
        When I visit "http://localhost:8080"
        And I set "foo" to "Hello world"
        And I note browser session
        Then "foo" is set to "Hello world"
        And I only used one browser session
