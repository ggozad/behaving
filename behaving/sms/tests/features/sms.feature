Feature: Send an SMS

    Scenario: Receive SMSs
        When I send an sms to 111 with body "Hello world"
        Then I should receive an sms at 111
        When I send an sms to 222 with body "Hello world"
        Then I should receive an sms at 222 containing "world"


