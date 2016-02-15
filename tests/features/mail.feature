Feature: Email steps

    @email
    Scenario: Receive email
        When I send an email to "foo@bar.com" with subject "Hello world" and body "Greetings from a BDD world!"
        Then I should receive an email at "foo@bar.com"
        And I should receive an email at "foo@bar.com" with subject "Hello world"
        But I should not receive an email at "foo@bar.com" with subject "Hello world and universe"
        And I should receive an email at "foo@bar.com" containing "BDD"
        But I should not receive an email at "foo@bar.com" containing "BDDE"

    @email
    Scenario: Send Receive email with non ANSII subject
        When I send an email to "foo@bar.com" with subject "φοο βαρ" and body "βαρ φοο"
        Then I should receive an email at "foo@bar.com"
        And I should receive an email at "foo@bar.com" with subject "φοο βαρ"
        And I should receive an email at "foo@bar.com" containing "βαρ φοο"

        When I send an email to "foo@bar.com" with subject "få bår" and body "bår få"
        Then I should receive an email at "foo@bar.com"
        And I should receive an email at "foo@bar.com" with subject "få bår"
        And I should receive an email at "foo@bar.com" containing "bår få"

    @email
    Scenario: Receive email with attachment
        When I send an email to "foo@bar.com" with subject "Hello world" and body "Greetings from a BDD world!" and attachment "test.txt"
        Then I should receive an email at "foo@bar.com" with attachment "test.txt"
        And I should not receive an email at "foo@bar.com" with attachment "test_2.txt"

    @email
    Scenario: Receive email with subject within timeout
        When I send an email to "foo@bar.com" with subject "Hello world" and body "Greetings from a BDD world!"
        Then I should receive an email at "foo@bar.com" with subject "Hello world" within 2 seconds

    @email
    Scenario: Receive email containing text within timeout
        When I send an email to "foo@bar.com" with subject "Hello world" and body "Greetings from a BDD world!"
        Then I should receive an email at "foo@bar.com" containing "BDD" within 2 seconds

    @email
    Scenario: Receive email with attachment within timeout
        When I send an email to "foo@bar.com" with subject "Hello world" and body "Greetings from a BDD world!" and attachment "test.txt"
        Then I should receive an email at "foo@bar.com" with attachment "test.txt" within 2 seconds

    @email
    Scenario: Not receive email with subject within timeout
        When I should not receive an email at "foo@bar.com" with subject "Hello world" within 2 seconds

    @email
    Scenario: Not receive email containing text within timeout
        When I should not receive an email at "foo@bar.com" containing "BDD" within 2 seconds

    @email
    Scenario: Not receive email with attachment within timeout
        When I should not receive an email at "foo@bar.com" with attachment "test.txt" within 2 seconds

    @email
    @web
    Scenario: Click link in an email
        Given a browser
        When I send an email to "foo@bar.com" with subject "Hello world" and body "Go to https://www.crypho.com"
        And I click the link in the email I received at "foo@bar.com"
        Then the browser's URL should be "https://www.crypho.com/"

    @email
    Scenario: Parse email and set persona variable
        Given "Foo" as the persona
        When I send an email to "foo@bar.com" with subject "Hello world" and body "You password is: 'hax0r'. Click here"
        And I parse the email I received at "foo@bar.com" and set "password is: '{password}'"
        Then "password" is set to "hax0r"

    @email
    Scenario: International friendly
        Given "Foo" as the persona
        When I send an email to "foo@bar.com" with subject "få bår" and body "bår få: 'hax0r'."
        Then I should receive an email at "foo@bar.com"
        And I should receive an email at "foo@bar.com" with subject "få bår"
        And I should receive an email at "foo@bar.com" containing "bår få"
        When I parse the email I received at "foo@bar.com" and set "få: '{password}'"
        Then "password" is set to "hax0r"

    @email
    Scenario: No messages received
        When I send an email to "foo@bar.com" with subject "foo" and body "bar"
        Then I should not have received any emails at "bar@foo.com"
