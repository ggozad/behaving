# behaving

_behaving_ is a web application testing framework for
Behavior-Driven-Development, based on
[behave](http://pypi.python.org/pypi/behave) and
[splinter](https://github.com/cobrateam/splinter).

_behave_ is written in Python and is similar to
[Cucumber](http://cucumber.io/).
_behaving_ adds the step-libraries for multi-user web/email/sms/gcm
interactions, and provides the Python _behaving_ namespace so that
independent step-libraries can work together.

Please refer to _behave_'s excellent
[documentation](http://behave.readthedocs.io/en/latest/) for a guide on
how to use it, how to write your custom steps and make it possible to
extend _behaving_.

## Hello world

Starting to use _behaving_ is pretty easy. Inside some python module,
add your _features_ consisting each of one or more scenarios. These
features are Gherkin language files with an extension of `.feature`. In
the same directory you should have a steps module which imports the
_behaving_ steps as well as your own custom steps (more on that later in
the setup\_ section) . Here's a basic example:

```gherkin
Feature: Text presence

    Background:
        Given a browser

    Scenario: Search for BDD
        When I visit "http://www.wikipedia.org/"
        And I fill in "search" with "BDD"
        And I press "go"
        Then I should see "Behavior-driven development" within 5 seconds
```

## Email, SMS & GCM (Google Cloud Messaging)

While the web is the focus of _behaving_, it also includes simple mocks
for a mail, SMS and a GCM server. These come with a small collection of
steps allowing you to do things like:

```gherkin
Feature: Email & SMS

    Scenario: Click link in an email
        Given a browser
        When I send an email to "foo@bar.com" with subject "Hello" and body "Try out this website at http://google.com"
        And I click the link in the email I received at "foo@bar.com"
        Then the browser's URL should be "http://google.com/"

    Scenario: Receive SMS with body
        When I send an sms to "+4745690001" with body "Hello world"
        Then I should receive an sms at "+4745690001" containing "world"

    Scenario: Receive GCM Notification
        When I send a gcm message "{"to":"deviceID", "data": {"message": "Foo Bar", "badge": 6}}"
        Then I should receive a gcm notification at "deviceID" containing "{'data': {'message': 'Foo Bar'}}"
```

Typically, it will be your web application that sends
email/sms/notifications and testing it comes down to configuring the
application to send email/sms/notifications to the mock servers.

## Personas & state

A lot of web apps today rely on multi-user interactions. To help you
with those interactions, _behaving_ uses the notion of _personas_. A
persona within a test runs in its own instance of a browser and you can
have more than one persona (and its browser instance) running
concurrently. You switch among personas by calling

```gherkin
Given "PersonaName" as the persona
```

Personas are also typically implemented as simple dictionaries allowing
them to carry state, save and reuse variables inside a scenario. When a
persona is first invoked it is created as an empty dictionary. You can
predefine personas though with set values.

Let's take the familiar LOTR characters as our test users. On setting up
the test environment (details later in the setup\_ section), we set up
the characters basic variables we might be needing in the tests as such:

```python
PERSONAS = {
    'Frodo': dict(
        fullname=u'Frodo Baggins',
        email=u'frodo@shire.com',
        password=u'frodopass',
        mobile='+4745690001',
        address: {
            street: "The Shire",
            zip: "4321"
        }
    ),
    'Gandalf': dict(
        fullname=u'Gandalf the Grey',
        email=u'gandalf@wizardry.com',
        password=u'gandalfpass',
        mobile='+4745690004',
        address: {
            street: "Rivendell street 1",
            zip: "1234"
        }
  ),
  ...
}
def before_scenario(context, scenario):
    ...
    context.personas = PERSONAS
```

Within a test and given a persona, you can now use `$var_name` to access
a variable of a persona. You can also set new variables on personas. So
the following,

```gherkin
Given "Gandalf" as the persona
When I fill in "name" with "$fullname"
And I fill in "street" with "$address.street"
And I set "title" to the text of "document-title"
And I fill in "delete" with "$title"
And I set "address.country" to the text of "country"
And I set "postaddress" to:
"""
$fullname
$address.street, $address.zip, $address.country
"""
```

would fill in the field with id `name` with `Gandalf the Grey`, `street`
with `Rivendell street 1` set the variable `title` to the text of the
element with id `document-title` and reuse the variable `title` to fill
in the field with id `delete`. It would also store the value of the
field with id "country" in address[`country`]. The `$var_name` pattern
is also usable in the text received by steps that expect a body of text,
which means that the `postaddress` persona variable will contain
Gandalf's complete snail-mail postage address nicely formatted on
multiple lines.

## Hello Persona example

Let us assume the following (coming from a real example) scenario.
[Crypho](https://crypho.com), is an online messaging/sharing site that
provides users with end-to-end encrypted real-time communications.
_behaving_ was written to help test Crypho.

In Crypho, teams collaborate in _spaces_. To invite somebody in a
_space_ the invitee has to share a token with an invitor, so both can
verify each other's identity.

```gherkin
Feature: Frodo invites Gandalf to The Shire space

    Given state "the-shire"

    Scenario: Frodo invites Gandalf to The Shire

        Given "Gandalf" as the persona
        When I log in
```

Before the scenarios start, the custom step `Given state "the-shire"`
executes. This preloads the db with data, sets up the server etc. Then
the scenario executes:

First Gandalf logs in. The step `Given "Gandalf" as the persona`, fires
up a browser that belongs to the persona Gandalf. The following step,
`When I log in` is a custom step defined as follows:

```python
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
```

Observe above how the current persona (Gandalf) parses the sms it
receives and saves it as "token". Later Gandalf reuses it to fill in the
two-factor authentication field.

Now that Gandalf is logged in, the test proceeds with Frodo. Frodo will
log in, and invite Gandalf to a private space.

```gherkin
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
```

Once the invitations are sent we switch back to Gandalf's browser, who
should have received a notification in his browser, as well as an email.
He then proceeds to send an sms to Frodo with the token who completes
the invitation.

```gherkin
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
```

You can see the test in action on video
[here](http://vimeo.com/63672466/).

There maybe instances where you require personas but do not want a
seperate browser associated with each persona, this can be achieved by
adding the attribute _single_browser_ to the context object (usually
performed in one of the hooks in `environment.py`), e.g:

```python
def before_scenario(context):
    context.single_browser = True
```

## Setting up a test environment

Start by installing _behaving_ by using either `pip` or `easy_install`.
This will also install dependencies and create the `behave` script with
which you invoke your tests. If you prefer using buildout, clone the
package itself from its repository, it contains already a buildout
configuration.

Typically you will be having a folder containing all your features and
steps. For example a directory structure like the following:

```
features/
features/mytest.feature
features/myothertest.feature
features/environment.py
features/steps/
features/steps/steps.py
```

In the steps directory you will need to import the _behaving_ steps you
need. You can also define your own steps. So `steps.py` might look like:

```python
from behave import when
from behaving.web.steps import *
from behaving.sms.steps import *
from behaving.mail.steps import *
from behaving.notifications.gcm.steps import *
from behaving.personas.steps import *

@when('I go to home')
def go_to_home(context):
    context.browser.visit('https://web/')
```

In `environment.py` you specify settings as well the things that need to
happen at various stages of testing, i.e. before and after everything, a
feature run, or a scenario run. For convenience you can import and reuse
`behaving.environment` which will perform default actions like closing
all browsers after a scenario, clean the email folder etc.

It is also possible to use `behaving.web.environment`,
`behaving.mail.environment`, `behaving.sms.environment` and
`behaving.personas.environment` on their own, if you don't have need for
SMS for example.

An example of an environment that does simply set some variables and
then rely on default actions for the various stages, might look like the
following:

```python
import os
from behaving import environment as benv

PERSONAS = {}

def before_all(context):
    import mypackage
    context.attachment_dir = os.path.join(os.path.dirname(mypackage.__file__), 'tests/data')
    context.sms_path = os.path.join(os.path.dirname(mypackage.__file__), '../../var/sms/')
    context.gcm_path = os.path.join(os.path.dirname(mypackage.__file__), '../../var/gcm/')
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
    context.personas = PERSONAS

def after_scenario(context, scenario):
    benv.after_scenario(context, scenario)
```

The following variables are supported and can be set to override
defaults:

- `screenshots_dir` (the path where screenshots will be saved. If it
  is set, any failure in a scenario will result in a screenshot of the
  browser at the time when the failure happened.)
- `attachment_dir` (the path where file attachments can be found)
- `sms_path` (the path to be used by `smsmock` to save sms. Defaults
  to `current_dir/sms` )
- `gcm_path` (the path to be used by `gcmmock` to save gcm
  notifications. Defaults to `current_dir/gcm` )
- `mail_path` (the path to be used by `mailmock` to save mail.
  Defaults to `current_dir/mail` )
- `default_browser`
- `default_browser_size` (tuple (width, height), applied to each
  browser as it's created)
- `max_browser_attempts` (how many times to retry creating the browser
  if it fails)
- `remote_webdriver_url` (points to your selenium hub url or remote
  webdriver. Defaults to `None`)
- `browser_args` (a dict of additional keyword arguments used when
  creating a browser)
- `base_url` (the base url for a browser, allows you to use relative
  paths)
- `accept_ssl_certs` (setting to `True` will accept self-signed/invalid
  certificates. Defaults to `None`)

You can run the tests simply by issuing

```sh
./bin/behave ./features
```

For chrome and docker issues, the code below is useful

```python
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
context.browser_args = {
    'options': chrome_options
}
```

## Mail, GCM and SMS mock servers

When _behaving_ is installed, it creates three scripts to help you test
mail, gcm and sms, `mailmock`, `gcmmock` and `smsmock` respectively. You
can directly invoke them before running your tests, they all take a port
as well as the directory to output data as parameters. For example,

```sh
./bin/smsmock -p 8081 -o ./var/sms
./bin/gcmmock -p 8082 -o ./var/notifications/gcm
./bin/mailmock -p 8083 -o ./var/mail [--no-stdout]
```

## `behaving.web` Supported matchers/steps

- Browsers

  - Given a browser [opens the default browser, i.e. Firefox]
  - Given `brand` as the default browser [sets the default browser to be `brand`, this is the browser name when using the remote webdriver or Firefox, Chrome, Safari]
  - Given the electron app "`app_path`" [for use with electron-based desktop apps]
  - Given browser "`name`" [opens the browser named `name`]
  - When I reload
  - When I go back
  - When I go forward
  - When I resize the browser to `width`x`height`
  - When I resize the viewport to `width`x`height`
  - When I take a screenshot [will save a screenshot of the browser if `screenshots_dir` is set on the environment. Also, if `screenshots_dir` is set, all failing tests will result in a screenshot.]
  - When I execute the script "`script`"
  - When I set the cookie "`key`" to "`value`"
  - When I delete the cookie "`key`"
  - When I delete all cookies
  - When I close the browser "`name`"

- Frames

  - When I switch to frame with css "`css`"
  - When I switch back to the main page

- Windows

  - When I open a new window named "`name`" at "`url`"
  - When I name the current window "`name`"
  - When I switch to the window named "`name`"

- URLs

  - Given the base url "`url`" [sets the base url to `url`, alternatively set `context.base_url` directly in `environment.py`]
  - When I visit "`url`"
  - When I go to "`url`"
  - When I parse the url path and set "`{expression}`"
  - Then the browser's URL should be "`url`"
  - Then the browser's URL should contain "`text`"
  - Then the browser's URL should not contain "`text`"

- Links

  - When I click the link to "`url`"
  - When I click the link to a url that contains "`url`"
  - When I click the link with text "`text`"
  - When I click the link with text that contains "`text`"

- Text, element & class presence

  - When I wait for `timeout` seconds
  - When I show the element with id "`id`"
  - When I hide the element with id "`id`"

  - Text

    - Then I should see "`text`"
    - Then I should not see "`text`"
    - Then I should see "`text`" within `timeout` seconds
    - Then I should not see "`text`" within `timeout` seconds

  - ID
    - Then I should see an element with id "`id`"
    - Then I should not see an element with id "`id`"
    - Then I should see an element with id "`id`" within `timeout` seconds
    - Then I should not see an element with id "`id`" within `timeout` seconds

- CSS

  - Existence
    - Then I should see an element with the css selector "`selector`"
    - Then I should not see an element with the css selector "`selector`"
    - Then I should see an element with the css selector "`selector`" within `timeout` seconds
    - Then I should not see an element with the css selector "`selector`" within `timeout` seconds
    - Then I should see `n` elements with the css selector "`css`"
    - Then I should see at least `n` elements with the css selector "`css`" within `timeout` seconds
  - Visibility
    - Then the element with the css selector "`css`" should be visible
    - Then the element with the css selector "`css`" should be visible within `timeout` seconds
    - Then the element with the css selector "`css`" should not be visible
    - Then the element with the css selector "`css`" should be visible within `timeout` seconds
    - Then {n:d} elements with the css selector "`css`" should be visible
    - Then {n:d} elements with the css selector "`css`" should be visible within `timeout` seconds
    - Then at least {n:d} elements with the css selector "`css`" should be visible
    - Then at least {n:d} elements with the css selector "`css`" should be visible within `timeout` seconds
  - Existence of a class on an element
    - Then the element with xpath "`xpath`" should have the class "`cls`"
    - Then the element with xpath "`xpath`" should not have the class "`cls`"
    - Then the element with xpath "`xpath`" should have the class "`cls`" within `timeout` seconds
    - Then the element with xpath "`xpath`" should not have the class "`cls`" within `timeout` seconds
    - Then "`name`" should have the class "`cls`"
    - Then "`name`" should not have the class "`cls`"
    - Then "`name`" should have the class "`cls`" within `timeout` seconds
    - Then "`name`" should not have the class "`cls`" within `timeout:d` seconds
  - XPath
    - Then I should see an element with xpath "`xpath`"
    - Then I should not see an element with xpath "`xpath`"
    - Then I should see an element with xpath "`xpath`" within `timeout` seconds
    - Then I should not see an element with xpath "`xpath`" within `timeout` seconds

- Forms

  - When I fill in "`name|id`" with "`value`"
  - When I clear field "`name|id`"
  - When I type "`value`" to "`name|id`" [same as fill, but happens slowly triggering keyboard events]
  - When I choose "`value`" from "`name`"
  - When I check "`name|id`"
  - When I uncheck "`name|id`"
  - When I toggle "`name|id`"
  - When I select "`value`" from "`name`""
  - When I select by text "`text`" from "`name`""
  - When I press "`name|id|text|innerText`"
  - When I press the element with xpath "`xpath`"
  - When I attach the file "`path`" to "`name`"
  - When I set the innner HTML of the element with id "`id`" to "`contents`" [Sets html on a `contenteditable` element with id `id` to `contents`]
  - When I set the innner HTML of the element with class "`class`" to "`contents`"
  - When I set the innner HTML of the element with class "`class`" to "`contents`"
  - When I send "`KEY`" to "`name`"
  - When I focus on "`name`"
  - Then field "`name`" should have the value "`value`"
  - Then field "`name`" should have the value "`value`" within `timeout` seconds
  - Then "`name`" should be enabled
  - Then "`name`" should be disabled
  - Then "`name`" should not be enabled
  - Then "`name`" should be valid
  - Then "`name`" should be invalid
  - Then "`name`" should not be valid
  - Then "`name`" should be required
  - Then "`name`" should not be required

- HTML tables

  - Then the table with id "`id`" should be  
    | header1 | header2 | ... | header(m) |  
    | cell00 | cell01 | ... | cell0m |  
    | cell10 | cell11 | ... | cell1m |  
    ...  
    | celln0 | celln1 | ... | cellnm |

  - Then the table with xpath "`xpath`" should be  
    | header1 | header2 | ... | header(m) |  
    | cell00 | cell01 | ... | cell0m |  
    | cell10 | cell11 | ... | cell1m |  
    ...  
    | celln0 | celln1 | ... | cellnm |

  - Then the table with id "`id`" should contain the rows  
    | cell00 | cell01 | ... | cell0m |  
    | cell10 | cell11 | ... | cell1m |

  - Then the table with xpath "`xpath`" should contain the rows  
    | cell00 | cell01 | ... | cell0m |  
    | cell10 | cell11 | ... | cell1m |

  - Then the table with id "`id`" should not contain the rows  
    | cell00 | cell01 | ... | cell0m |  
    | cell10 | cell11 | ... | cell1m |

  - Then the table with xpath "`xpath`" should not contain the rows  
    | cell00 | cell01 | ... | cell0m |  
    | cell10 | cell11 | ... | cell1m |

  - Then row `row_no` in the table with id "`id`" should be  
    | cell00 | cell01 | ... | cell0m |

  - Then row `row_no` in the table with xpath "`xpath`" should be  
    | cell00 | cell01 | ... | cell0m |

  - Then the value of the cell in row `row_no`, column `col_no` in the table with id "`id`" should be "`value`"

  - Then the value of the cell in row `row_no`, column `col_no` in the table with xpath "`xpath`" should be "`value`"

  - Then the value of the cell in row `row_no`, column "`col_header`" in the table with id "`id`" should be "`value`"

  - Then the value of the cell in row `row_no`, column "`col_header`" in the table with xpath "`xpath`" should be "`value`"

- Alerts & prompts

  - When I enter "`text`" to the alert - When I accept the alert - When I dismiss the alert - Then I should see an alert - Then I should see an alert within `timeout` seconds - Then I should see an alert containing "`text`" - Then I should see an alert containing "`text`" within `timeout` seconds

- Mouse

  - When I mouse over the element with xpath "`xpath`"
  - When I mouse out of the element with xpath "`xpath`"

- Downloads

  - Then the file "`filename`" with contents "`text`" should have been downloaded within `timeout` seconds
  - Then the file "`filename`" should have been downloaded within `timeout` seconds

- Persona interaction & variables

  - When I set "`key`" to the text of "`id|name`"
  - When I set "`key`" to the attribute "`attr`" of the element with xpath "`xpath`"
  - When I evaluate the script "`script`" and assign the result to "`key`"

## `behaving.mail` Supported matchers/steps

- When I click the link in the email I received at "`address`"
- When I parse the email I received at "`address`" and set "`expression`"
- When I clear the email messages
- Then I should receive an email at "`address`"
- Then I should receive an email at "`address`" with subject "`subject`"
- Then I should receive an email at "`address`" containing "`text`"
- Then I should receive an email at "`address`" with attachment "`filename`"
- Then I should not have received any emails at "`address`"

## `behaving.sms` Supported matchers/steps

- When I set "`key`" to the body of the sms I received at "`number`"
- When I parse the sms I received at "`number`" and set "`expression`"
- Then I should receive an sms at "`number`"
- Then I should receive an sms at "`number`" containing "`text`"

## `behaving.notifications.gcm` Supported matchers/steps

- When I send a gcm message "{"to":"deviceID", "data": {"message":"Foo Bar", "badge": 6}}"
- Then I should receive a gcm notification at "deviceID" containing "{'data': {'message': 'Foo Bar'}}"
- Then I should have received any gcm notifications at "deviceID"

## `behaving.personas` Supported matchers/steps

- Given "`name`" as the persona
- When I set "`key`" to "`value`"
- When I set "`key`" to:  
  """ `some longer body of text`  
   `usually multiline`  
  """
- When I clone persona "`source`" to "`target`"
- Then "`key`" is set to "`value`"

## Debugging

- When I pause the tests

## Docker integration

A `Dockerfile` as well as a complete setup using `docker-compose` are provided to help you create selenium grid configurations that run your tests. In addition dev container configuration is included if VSCode is your thing.

In addition we provide pre-build images on docker hub for the `linux/amd64` and `linux/arm64` platforms. Use

```bash
docker pull behaving/behaving:latest
```

to pull the image.

## Running behaving tests

You can run all behaving tests as follows:

Start docker compose:

```
docker-compose up
```

Open a shell in the behaving container:

```
docker-compose exec behaving bash
```

Run behaving tests:

```
behave tests/features
```
