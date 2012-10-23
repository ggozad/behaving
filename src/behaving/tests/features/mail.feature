Feature: Email steps

    @email
    Scenario: Receive email
        When I send an email to foo@bar.com with subject "Hello world" and body "Greetings from a BDD world!"


