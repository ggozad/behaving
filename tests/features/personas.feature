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
    Scenario: Set variables text
        Given "Foo" as the persona
        When I set "foo" to:
            """
            Hello wørld
            """
        And I set "bar" to "Hello wørld"
        Then "foo" is set to "$bar"
        When I set "foo" to "wørld"
        And I set "bar" to:
            """
            Hello $foo
            """
        Then "bar" is set to "Hello wørld"



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
    Scenario: Clone persona
        Given "Foo" as the persona
        When I set "bar" to "Hello world"
        When I clone persona "Foo" to "FooClone"
        Given "FooClone" as the persona
        Then "bar" is set to "Hello world"
