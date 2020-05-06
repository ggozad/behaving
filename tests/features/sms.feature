Feature: Send an SMS

    @sms
    Scenario: Receive SMSs
        When I send an sms to "+4745690111" with body "foø"
        Then I should receive an sms at "+4745690111"

    @sms
    Scenario: Receive SMS with body
        When I send an sms to "222" with body "Hello wørld"
        And I send an sms to "222" with body "foø"
        Then I should receive an sms at "222" containing "wørld"
        And I should receive an sms at "222" containing "foø"

    @sms
    @personas
    Scenario: Persona variables from sms
        Given "Foo" as the persona
        When I send an sms to "111" with body "Hello wørld"
        And I set "foo" to the body of the sms I received at "111"
        Then "foo" is set to "Hello wørld"
        When I send an sms to "111" with body "You password is: 'haxør'. Click here"
        And I parse the sms I received at "111" and set "password is: '{password}'"
        Then "password" is set to "haxør"
