behaving
========

`behaving` is a web application testing framework for Behavior-Driver-Development, similar to `Cucumber`_ or `lettuce`_. It differs from these by focusing on multi-user web/email/sms interactions.

`behaving` is written in python and is based on `behave`_. Please refer to `behave`'s ' excellent `documentation <http://pythonhosted.org/behave/>`_ for a guide on how to use it, how to write your custom steps and make it possible to extend `behaving`.

Hello world
-----------

Starting using `behaving` is pretty easy. Inside some python module, add your *features* consisting each of one or more scenarios. These features are Gherkin language files with an extension of `.feature`. In the same directory you should have a steps module which imports the `behaving` steps as well as your own custom steps. Here's a basic example:

::

    Feature: Text presence

        Background:
            Given a browser

        Scenario: Search for BDD
            When I visit "http://www.wikipedia.org/"
            And I fill in "search" with "BDD"
            And I press "go"
            Then I should see "Behavior-driven development" within 5 seconds

Email & SMS
-----------

While the web is the focus of `behaving`, it also includes simple mocks for a mail and an SMS server. These come with a small collection of steps allowing you to do things like:

::

    Feature: Email & SMS

        Scenario: Click link in an email
            Given a browser
            When I send an email to "foo@bar.com" with subject "Crypho" and body "Try out our product at http://crypho.com"
            And I click the link in the email I received at "foo@bar.com"
            Then the browser's URL should be "http://crypho.com/"

        Scenario: Receive SMS with body
            When I send an sms to "+4745690001" with body "Hello world"
            Then I should receive an sms at "+4745690001" containing "world"

Typically of course, it will be your web application that sends mail/sms.

Personas & state
----------------

A lot of web apps today rely on multi-user interactions. To help you with those interactions, `behaving` uses the notion of *personas*. A persona has its own browser, and is implemented as a simple dictionary allowing it to carry state. A persona can therefore save state in variables and reuse it inside a scenario.

Let us assume the following (coming from a real example) scenario. `Crypho`_, is an online messaging/sharing site that provides users with end-to-end encrypted real-time communications. `behaving` was written to help test Crypho.

You can see the test in action on video `here <http://vimeo.com/62777458/>`_.

In Crypho, to invite somebody in a *space* the invitee has to share a token with an invitor, so both can verify each other's identity.

::

    Feature: Frodo invites Gandalf to The Shire space

        Given state "the-shire"

        Scenario: Frodo invites Gandalf to The Shire

            Given "Gandalf" as the persona
            When I log in

Before the scenarios start, the custom step `Given state "the-shire"` executes. This preloads the db with data sets up the server etc. Then the scenario executes:

First Gandalf logs in. The step `Given "Gandalf" as the persona`, fires up a browser that belongs to the persona Gandalf. The following step, `When I log in` is a custom step defined as follows:

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

Observe above how the current persona (Gandalf) parses the sms it receives and saves it as "token". Later Gandalf reuses it to fill in the two-factor authentication field.

Now that Gandalf is logged in, the test proceeds with Frodo. Frodo will log in, and invite Gandalf to a private space.

::

            Given "Frodo" as the persona
            When I log in
            And I click the link with text that contains "My spaces"
            And I click the link with text that contains "The Shire"
            And I press "invite-members"
                Then I should see "Invite members" within 1 seconds
            When I fill in "invitees" with "gandalf@wizardry.com"
            And I fill in "invitation-message" with "Come and join us!"
            And I press "send-invitations"
                Then I should see "Your invitations have been sent" within 2 seconds


Once the invitations are sent we switch back to Gandalf's browser, who should have received a notification in his browser, as well as an email. He then proceeds to send an sms to Frodo with the token who completes the invitation.

::

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
