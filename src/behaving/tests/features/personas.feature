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
        When I set "mydict.foo" to "aaa"

    @personas
    Scenario: Escaped persona variables
        Given "Foo" as the persona
        When I set "foo" to "\$1.00"
        And I set "bar" to "$foo Dollars"
        Then "bar" is set to "\$1.00 Dollars"
        And "bar" is set to "$foo Dollars"
        When I set "bar" to "\$1.00 Dollars"
        Then "bar" is set to "\$1.00 Dollars"
        And "bar" is set to "$foo Dollars"


    @personas
    Scenario: Don't start up multiple browsers
        Given I enable single browser mode
        And browser "foobar"
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

    @personas
    Scenario: Clone persona
        Given "Foo" as the persona
        When I set "bar" to "Hello world"
        When I clone persona "Foo" to "FooClone"
        Given "FooClone" as the persona
        Then "bar" is set to "Hello world"
