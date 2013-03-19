behaving
========

`behaving` is a web application testing framework for Behavior-Driver-Development, similar to `Cucumber`_ or `lettuce`_. It differs from these by focusing on multi-user web/email/sms interactions which are essential to web application building.

Example
-------

`behaving` is best explained by example:



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

