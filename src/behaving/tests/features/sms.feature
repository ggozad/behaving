Feature: Send an SMS

    @sms
    Scenario: Receive SMSs
        When I send an sms to "111" with body "Hello world"
        Then I should receive an sms at "111"
        When I send an sms to "222" with body "Hello world"
        Then I should receive an sms at "222" containing "world"

    @sms, @personas
    Scenario: Persona variables from sms
        Given "Foo" as the persona
        When I send an sms to "111" with body "Hello world"
        And I set "foo" to the body of the sms I received at "111"
        Then "foo" is set to "Hello world"