behaving
========

*behaving* is a web application testing framework for Behavior-Driven-Development, similar to `Cucumber`_ or `lettuce`_. It differs from these by focusing on multi-user web/email/sms interactions.

*behaving* is written in python and is based on `behave`_ and `splinter`_. Please refer to *behave*'s excellent `documentation <http://pythonhosted.org/behave/>`_ for a guide on how to use it, how to write your custom steps and make it possible to extend *behaving*.

Hello world
-----------

Starting to use *behaving* is pretty easy. Inside some python module, add your *features* consisting each of one or more scenarios. These features are Gherkin language files with an extension of ``.feature``. In the same directory you should have a steps module which imports the *behaving* steps as well as your own custom steps (more on that later in the setup_ section) . Here's a basic example:

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

While the web is the focus of *behaving*, it also includes simple mocks for a mail and an SMS server. These come with a small collection of steps allowing you to do things like:

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

Typically, it will be your web application that sends email/sms and testing it comes down to configuring the application to send email/sms to the mock servers.

Personas & state
----------------

A lot of web apps today rely on multi-user interactions. To help you with those interactions, *behaving* uses the notion of *personas*. A persona within a test runs in its own instance of a browser and you can have more than one persona (and its browser instance) running concurrently. You switch among personas by calling

::

    Given "PersonaName" as the persona

Personas are also typically implemented as simple dictionaries allowing them to carry state, save and reuse variables inside a scenario. When a persona is first invoked it is created as an empty dictionary. You can predefine personas though with set values.

Let's take the familiar LOTR characters as our test users. On setting up the test environment (details later in the setup_ section), we set up the characters basic variables we might be needing in the tests as such:

::

    PERSONAS = {
        'Frodo': dict(
                fullname=u'Frodo Baggins',
                email=u'frodo@shire.com',
                password=u'frodopass',
                mobile='+4745690001'
            ),

        'Gandalf': dict(
                fullname=u'Gandalf the Grey',
                email=u'gandalf@wizardry.com',
                password=u'gandalfpass',
                mobile='+4745690004'
            ),
        ...
    }

    def before_all(context):
        ...
        context.personas = PERSONAS


Within a test and given a persona, you can now use ``$var_name`` to access a variable of a persona. You can also set new variables on personas. So the following,

::

    Given "Gandalf" as the persona
    When I fill in "name" with "$fullname"
    And I set "title" to the text of "document-title"
    And I fill in "delete" with "$title"

would fill in the field with id ``name`` with ``Gandalf the Grey``, set the variable ``title`` to the text of the element with id ``document-title`` and reuse the variable ``title`` to fill in the field with id ``delete``.

Hello Persona example
---------------------

Let us assume the following (coming from a real example) scenario. `Crypho`_, is an online messaging/sharing site that provides users with end-to-end encrypted real-time communications. *behaving* was written to help test Crypho.

In Crypho, teams collaborate in *spaces*. To invite somebody in a *space* the invitee has to share a token with an invitor, so both can verify each other's identity.

::

    Feature: Frodo invites Gandalf to The Shire space

        Given state "the-shire"

        Scenario: Frodo invites Gandalf to The Shire

            Given "Gandalf" as the persona
            When I log in

Before the scenarios start, the custom step ``Given state "the-shire"`` executes. This preloads the db with data, sets up the server etc. Then the scenario executes:

First Gandalf logs in. The step ``Given "Gandalf" as the persona``, fires up a browser that belongs to the persona Gandalf. The following step, ``When I log in`` is a custom step defined as follows:

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

You can see the test in action on video `here <http://vimeo.com/63672466/>`_.

.. _setup:

Setting up a test environment
-----------------------------

Start by installing *behaving* by using either ``pip`` or ``easy_install``. This will also install dependencies and create the ``behave`` script with which you invoke your tests. If you prefer using buildout, clone the package itself from its repository, it contains already a buildout configuration.

Typically you will be having a folder containing all your features and steps. For example a directory structure like the following:

::

    features/
    features/mytest.feature
    features/myothertest.feature
    features/environment.py
    features/steps/
    features/steps/steps.py

In the steps directory you will need to import the *behaving* steps you need. You can also define your own steps. So ``steps.py`` might look like:

::

    from behave import when
    from behaving.web.steps import *
    from behaving.sms.steps import *
    from behaving.mail.steps import *
    from behaving.personas.steps import *

    @when('I go to home')
    def go_to_home(context):
        context.browser.visit('https://localhost:8080/')

In ``environment.py`` you specify settings as well the things that need to happen at various stages of testing, i.e. before and after everything, a feature run, or a scenario run. For convenience you can import and reuse ``behaving.environment`` which will perform default actions like closing all browsers after a scenario, clean the email folder etc.

It is also possible to use ``behaving.web.environment``, ``behaving.mail.environment``, ``behaving.sms.environment`` and ``behaving.personas.environment`` on their own, if you don't have need for SMS for example.

An example of an environment that does simply set some variables and then rely on default actions for the various stages, might look like the following:

::

    import os
    from behaving import environment as benv


    def before_all(context):
        import mypackage
        context.attachment_dir = os.path.join(os.path.dirname(mypackage.__file__), 'tests/data')
        context.sms_path = os.path.join(os.path.dirname(mypackage.__file__), '../../var/sms/')
        context.mail_path = os.path.join(os.path.dirname(mypackage.__file__), '../../var/mail/')
        benv.before_all(context)


    def after_all(context):
        benv.after_all(context)


    def before_feature(context, feature):
        benv.before_feature(context, feature)


    def after_feature(context, feature):
        benv.after_feature(context, feature)


    def before_scenario(context, scenario):
        benv.before_scenario(context, scenario)


    def after_scenario(context, scenario):
        benv.after_scenario(context, scenario)

The following variables are supported and can be set to override defaults:

* ``attachment_dir`` (the path where file attachments can be found)
* ``sms_path`` (the path to be used by ``smsmock`` to save sms. Defaults to ``current_dir/sms`` )
* ``mail_path`` (the path to be used by ``mailmock`` to save mail. Defaults to ``current_dir/mail`` )
* ``default_browser``
* ``remote_webdriver`` (whether to use the remote webdriver. Defaults to ``False``)
* ``browser_args`` (a dict of additional keyword arguments used when creating a browser)
* ``base_url``

You can run the tests simply by issuing

::

    ./bin/behave ./features

Mail and SMS mock servers
-------------------------

When *behaving* is installed, it creates two scripts to help you test mail and sms, ``mailmock`` and ``smsmock`` respectively. You can directly invoke them before running your tests, they both take a port as well as the directory to output data as parameters. For example,

::

    ./bin/smsmock -p 8081 -o ./var/sms
    ./bin/mailmock -p 8082 -o ./var/mail


``behaving.web`` Supported matchers/steps
-----------------------------------------

* Browsers

    * Given a browser
      [opens the default browser, i.e. Firefox]
    * Given ``brand`` as the default browser
      [sets the default browser to be ``brand``, this is the browser name when using the remote webdriver or Firefox, Chrome, Safari or PhantomJS]
    * Given browser "``name``"
      [opens the browser named ``name``]
    * When I reload
    * When I go back
    * When I go forward

* URLs

    * Given the base url "``url``"
      [sets the base url to ``url``, alternatively set ``context.base_url`` directly in ``environment.py``]
    * When I visit "``url``"
    * When I go to "``url``"
    * When I parse the url path and set "``{expression}``"
    * Then the browser's url should be "``url``"
    * Then the browser's url should contain "``text``"
    * Then the browser's url should not contain "``text``"

* Links

    * When I click the link to "``url``"
    * When I click the link to a url that contains "``url``"
    * When I click the link with text "``text``"
    * When I click the link with text that contains "``text``"

* Text & element presence

    * When I wait for ``timeout`` seconds
    * When I show the element with id "``id``"
    * When I hide the element with id "``id``"
    * Then I should see "``text``"
    * Then I should not see "``text``"
    * Then I should see "``text``" within ``timeout`` seconds
    * Then I should not see "``text``" within ``timeout`` seconds
    * Then I should see an element with id "``id``"
    * Then I should not see an element with id "``id``"
    * Then I should see an element with id "``id``" within ``timeout`` seconds
    * Then I should not see an element with id "``id``" within ``timeout`` seconds
    * Then I should see an element with the css selector "``selector``"
    * Then I should not see an element with the css selector "``selector``"
    * Then I should see an element with the css selector "``selector``" within ``timeout`` seconds
    * Then I should not see an element with the css selector "``selector``" within ``timeout`` seconds
    * Then I should see an element with xpath "``xpath``"
    * Then I should not see an element with xpath "``xpath``"
    * Then I should see an element with xpath "``xpath``" within ``timeout`` seconds
    * Then I should not see an element with xpath "``xpath``" within ``timeout`` seconds

* Forms

    * When I fill in "``name``" with "``value``"
    * When I type "``value``" to "``name``"
      [same as fill, but happens slowly triggering keyboard events]
    * When I choose "``value``" from "``name``"
    * When I check "``name``"
    * When I uncheck "``name``"
    * When I select "``value``" from "``name``""
    * When I press "``name|id|text|innerText``"
    * When I press the element with xpath "``xpath``"
    * When I attach the file "``path``" to "``name``"
    * When I set the innner HTML of the element with id "``id``" to "``contents``"
      [Sets html on a ``contenteditable`` element with id ``id`` to ``contents``]
    * When I set the innner HTML of the element with class "``class``" to "``contents``"
    * When I set the innner HTML of the element with class "``class``" to "``contents``"
    * Then field "``name``" should have the value "``value``"
    * Then "``name``" should be enabled
    * Then "``name``" should be disabled
    * Then "``name``" should not be enabled
    * Then "``name``" should be valid
    * Then "``name``" should be invalid
    * Then "``name``" should not be valid
    * Then "``name``" should be required
    * Then "``name``" should not be required

* Persona interaction & variables

    * Given "``name``" as the user
      [opens a reusable browser named ``name``)
    * When I set "``key``" to the text of "``id|name``"
    * When I set "``key``" to the attribute "``attr``" of the element with xpath "``xpath``"

``behaving.mail`` Supported matchers/steps
------------------------------------------

* When I click the link in the email I received at "``address``"
* Then I should receive an email at "``address``"
* Then I should receive an email at "``address``" with subject "``subject``"
* Then I should receive an email at "``address``" containing "``text``"

``behaving.sms`` Supported matchers/steps
-----------------------------------------

* When I set "``key``" to the body of the sms I received at "``number``"
* When I parse the sms I received at "``number``" and set "``expressions``"
* Then I should receive an sms at "``number``"
* Then I should receive an sms at "``number``" containing "``text``"

``behaving.personas`` Supported matchers/steps
----------------------------------------------

* Given "``name``" as the persona
* When I set "``key``" to "``value``"
* Then "``key``" is set to "``value``"

.. _`Cucumber`: http://cukes.info/
.. _`lettuce`: http://lettuce.it/
.. _`behave`: http://pypi.python.org/pypi/behave
.. _`splinter`: http://splinter.cobrateam.info/
.. _`Crypho`: http://crypho.com

