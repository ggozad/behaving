behaving.web
==========

`behaving.web` provides *steps* useful for testing web applications with `behave`_.
The package is pretty experimental, contributions are most welcome.


Supported matchers/steps
------------------------

    * Browsers

        * *Given a browser* (uses the default `splinter` browser, i.e. Firefox)
        * *Given Chrome as the browser* (selects chrome to run the tests)
        * *Given Firefox as the browser* (selects firefox to run the tests)
        * *When I reload* (reloads the current browser)
        * *When I go back* (clicks the browser's back button)
        * *When I go forward* (clicks the browser's forward button)

    * URLs

        * *Given the base url "url"* (sets the base url to `url`, alternatively set `context.base_url` directly in `environment.py`)
        * *When I visit "url"*
        * *When I go to "url"* (opens `url`)
        * *Then the browser's url should be "url"* (asserts the url is `url`)
        * *Then the browser's url should contain "text"* (asserts the url contains `text`)
        * *Then the browser's url should not contain "text"* (asserts the url does not contain `text`)

    * Links

        * *When I click the link to "url"* (clicks the link pointing to `url`)
        * *When I click the link to a url that contains "url"* (clicks the first link which points to a url containing `url`)
        * *When I click the link with text "text"* (clicks the first link with text `text`)
        * *When I click the link with text that contains "text"* (clicks the first link that contains `text`)

    * Text & element presence

        * *Then I should see "text"* (asserts `text` is present and visible)
        * *Then I should not see "text"* (asserts `text` is present and visible)
        * *Then I should see "text" within timeout seconds* (asserts `text` is present and visible within `timeout` seconds)
        * *Then I should not see "text" within timeout seconds* (asserts `text` is not present and visible within `timeout` seconds)
        * *Then I should see an element with id "id"* (asserts the element with `id` is present and visible)
        * *Then I should not see an element with id "id"* (asserts the element with `id` is not present and visible)
        * *Then I should see an element with id "id" within timeout seconds* (asserts the element with `id` is present and visible within `timeout` seconds)
        * *Then I should not see an element with id "id" within timeout seconds* (asserts the element with `id` is not present and visible within `timeout` seconds)
        * *Then I should see an element with the css selector "{css}"* (asserts the first element found by the `css` selector is present and visible)
        * *Then I should not see an element with the css selector "{css}"* (asserts the first element found by the `css` selector is not present and visible)
        * *Then I should see an element with the css selector "css" within timeout seconds* (asserts the first element found by the `css` selector is present and visible within `timeout` seconds)
        * *Then I should not see an element with the css selector "css" within timeout seconds* (asserts the first element found by the `css` selector is not present and visible within `timeout` seconds)

    * Forms

        * *When I fill in "name" with "value"* (Fills the control with name `name` with value `value`)
        * *When I choose "value" from "name*
        * *When I check "name"*
        * *When I uncheck "name"*
        * *When I select "value" from "name"*
        * *When I press "name"*

    * Multiple-user interaction

        * *Given "name" as the user* (opens a reusable browser that is used by user `name`)



    .. _`behave`: http://pypi.python.org/pypi/behave

