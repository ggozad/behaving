Feature: Send an SMS

    @sms
    Scenario: Receive SMSs
        When I send an sms to "+4745690111" with body "foo"
        Then I should receive an sms at "+4745690111"

    @sms
    Scenario: Receive SMS with body
        When I send an sms to "222" with body "Hello world"
        Then I should receive an sms at "222" containing "world"

    @sms
    @personas
    Scenario: Persona variables from sms
        Given "Foo" as the persona
        When I send an sms to "111" with body "Hello world"
        And I set "foo" to the body of the sms I received at "111"
        Then "foo" is set to "Hello world"
        When I send an sms to "111" with body "You password is: 'hax0r'. Click here"
        And I parse the sms I received at "111" and set "password is: '{password}'"
        Then "password" is set to "hax0r"
