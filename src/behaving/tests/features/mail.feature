Feature: Email steps

    @email
    Scenario: Receive email
        When I send an email to "foo@bar.com" with subject "Hello world" and body "Greetings from a BDD world!"
        Then I should receive an email at "foo@bar.com"
        And I should receive an email at "foo@bar.com" with subject "Hello world"
        And I should receive an email at "foo@bar.com" containing "BDD"

    @email 
    Scenario: Send Receive email with non ANSII subject
        When I send an email to "foo@bar.com" with encoded in "iso8859_7" subject "Γειά σου και χαρά σου"  and body "Χαιρετίσματα απο τη Σίφνο"
        Then I should receive an email at "foo@bar.com"
        And I should receive an email at "foo@bar.com" with subject "Γειά σου και χαρά σου"
        And I should receive an email at "foo@bar.com" containing "Χαιρετίσματα απο τη Σίφνο"

        When I send an email to "foo@bar.com" with encoded in "iso8859_10" subject "Korleis har du det?/Korleis går det?"  and body "Det er bedre å dø stående enn å leve på knærne."
        Then I should receive an email at "foo@bar.com"
        And I should receive an email at "foo@bar.com" with subject "Det er bedre å dø stående enn å leve på knærne."
        And I should receive an email at "foo@bar.com" containing "BDD"


    @email
    Scenario: Receive email with attachment
        When I send an email to "foo@bar.com" with subject "Hello world" and body "Greetings from a BDD world!" and attachment "test.txt"
        Then I should receive an email at "foo@bar.com" with attachment "test.txt"

    @email
    @web
    Scenario: Click link in an email
        Given a browser
        When I send an email to "foo@bar.com" with subject "Hello world" and body "Go to http://www.crypho.com"
        And I click the link in the email I received at "foo@bar.com"
        Then the browser's URL should be "http://www.crypho.com/"

    @email
    Scenario: Parse email and set persona variable
        Given "Foo" as the persona
        When I send an email to "foo@bar.com" with subject "Hello world" and body "You password is: 'hax0r'. Click here"
        And I parse the email I received at "foo@bar.com" and set "password is: '{password}'"
        Then "password" is set to "hax0r"
