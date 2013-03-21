behaving
========

`behaving` is a web application testing framework for Behavior-Driver-Development, similar to `Cucumber`_ or `lettuce`_. It differs from these by focusing on multi-user web/email/sms interactions.

`behaving` is written in python and is based on `behave`_. Please refer to `behave`'s ' excellent `documentation <http://pythonhosted.org/behave/>`_ for a guide on how to use it, how to write your custom steps and make it possible to extend `behaving`.

Personas
--------
To allow for easy multi-user interaction testing, `behaving` uses the notion of *personas*.

Example
-------

`behaving` is best explained by example. As is the case with most BDD frameworks, you write your tests using the Gherkin conventions.

Let us assume the following (coming from a real example) scenario. `Crypho`_, is an online messaging/sharing site that provides users with encrypted real-time communications. In Crypho, to invite somebody in a *space* the invitee has to share a token with an invitor, so both can verify each other's identity.

::

    Feature: Frodo invites Gandalf to The Shire space

        Scenario: Frodo invites Gandalf to The Shire

            Given "Gandalf" as the persona
            When I log in

Here, first Gandalf logs in. The step `Given "Gandalf" as the persona`, fires up a browser that belongs to the persona Gandalf. The following step, `When I log in` is a custom step defined as such:

::

    @when('I log in')
    def log_in(context):

        assert context.persona
        context.execute_steps(u"""
            When I go to Home
                Then I should see an element with id "email" within 2 seconds
            When I fill in "email" with "$email"
            And I press "send-sms"
                Then I should see "We have sent you an SMS with a security code" within 2 seconds
                And I should receive an sms at "$mobile"
                And "token" should be enabled
            When I parse the sms I received at "$mobile" and set "Your Crypho code is {token}"
            And I fill in "token" with "$token"
            And I fill in "password" with "$password"
            And I press "login"
                Then I should see "Crypho" within 5 seconds
        """)

asdasd
::

            Given "Frodo" as the persona
            When I log in
            And I click the link with text that contains "My spaces"
            And I click the link with text that contains "The Shire"
            And I press "invite-members"
                Then I should see "Invite members" within 2 seconds
            When I fill in "invitees" with "gandalf@wizardry.com"
            And I fill in "invitation-message" with "Come and join us!"
            And I press "send-invitations"
                Then I should see "Your invitations have been sent" within 2 seconds

            Given "Gandalf" as the persona
            Then I should see "Your invitations have been updated" within 2 seconds
            And I should receive an email at "gandalf@wizardry.com" containing "Frodo Baggins has invited you to join a private workspace in Crypho"
            When I click the link with text that contains "Invitations"
            And I click the link with text that contains "Pending invitations"
                Then I should see "Come and join us!"
            When I set "token" to the text of "invitation-token"
            And I send an sms to "45699900" with body "$token"

            Given "Frodo" as the persona
                Then I should receive an sms at "45699900"
            When I set "FrodoToken" to the body of the sms I received at "45699900"
            And I click the link with text that contains "Invitations"
            And I click the link with text that contains "Enter authorization token"
            And I fill in "auth-token" with "$FrodoToken"
            And I press "Submit"
                Then I should see "The invitation has been accepted." within 5 seconds
                And I should see "Gandalf the Grey has joined the space, invited by Frodo Baggins" within 10 seconds



`behaving.web` Supported matchers/steps
---------------------------------------

    * Browsers

        * Given a browser
            [opens the default browser, i.e. Firefox]
        * Given Chrome as the browser
        * Given Firefox as the browser
        * When I reload
        * When I go back
        * When I go forward

    * URLs

        * Given the base url "`url`"
            [sets the base url to `url`, alternatively set `context.base_url` directly in `environment.py`]
        * When I visit "`url`"
        * When I go to "`url`"
        * Then the browser's url should be "`url`"
        * Then the browser's url should contain "`text`"
        * Then the browser's url should not contain "`text`"

    * Links

        * When I click the link to "`url`"
        * When I click the link to a url that contains "`url`"
        * When I click the link with text "`text`"
        * When I click the link with text that contains "`text`"

    * Text & element presence

        * When I wait for `timeout` seconds
        * When I show the element with id "`id`"
        * When I hide the element with id "`id`"
        * Then I should see "`text`"
        * Then I should not see "`text`"
        * Then I should see "`text`" within `timeout` seconds
        * Then I should not see "`text`" within `timeout` seconds
        * Then I should see an element with id "`id`"
        * Then I should not see an element with id "`id`"
        * Then I should see an element with id "`id`" within `timeout` seconds
        * Then I should not see an element with id "`id`" within `timeout` seconds
        * Then I should see an element with the css selector "`selector`"
        * Then I should not see an element with the css selector "`selector`"
        * Then I should see an element with the css selector "`selector`" within `timeout` seconds
        * Then I should not see an element with the css selector "`selector`" within `timeout` secondss)

    * Forms

        * When I fill in "`name`" with "`value`"
        * When I choose "`value`" from "`name`"
        * When I check "`name`"
        * When I uncheck "`name`"
        * When I select "`value`" from "`name`""
        * When I press "`name|id|text|innerText`"
        * When I set the innner HTML of the element with id "`id`" to "`contents`"
            [Sets html on a `contenteditable` element with id `id` to `contents`]
        * When I set the innner HTML of the element with class "`class`" to "`contents`"

    * Persona interaction

        * Given "`name`" as the user
            [opens a reusable browser to be used by user `name`)
        * When I set "`key`" to the text of "`id|name`"


`behaving.mail` Supported matchers/steps
----------------------------------------

    * When I click the link in the email I received at "`address`"
    * Then I should receive an email at "`address`"
    * Then I should receive an email at "`address`" with subject "`subject`"
    * Then I should receive an email at "`address`" containing "`text`"

`behaving.sms` Supported matchers/steps
---------------------------------------

    * When I set "`key`" to the body of the sms I received at "`number`"
    * When I parse the sms I received at "`number`" and set "`expressions`"
    * Then I should receive an sms at "`number`"
    * Then I should receive an sms at "`number`" containing "`text`"

`behaving.personas` Supported matchers/steps
--------------------------------------------

    * Given "`name`" as the persona
    * When I set "`key`" to "`value`"
    * Then "`key`" is set to "`value`"

    .. _`Cucumber`: http://cukes.info/
    .. _`lettuce`: http://lettuce.it/
    .. _`behave`: http://pypi.python.org/pypi/behave
    .. _`Crypho`: http://crypho.com
