Feature: Send an SMS

    Scenario: Receive SMSs
        When I send an sms to 123456 with body "Hello world"
        Then I should receive an sms at 123456
