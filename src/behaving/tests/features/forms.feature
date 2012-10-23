Feature: Forms

    Background:
        Given a browser

    @web
    Scenario: Filling-in fields
        When I visit "http://localhost:8080/forms.html"
        And I fill in "name" with "Foo Bar"
        And I fill in "passwd" with "hax0r"
        And I choose "male" from "sex"
        And I check "subscribe"
        And I uncheck "digest"
        And I select "no" from "countries"
        And I select "gr" from "countries"
        And I attach the file "test.txt" to "file"
        And I press "register"
        Then the browser's URL should contain "name=Foo+Bar"
        And the browser's URL should contain "passwd=hax0r"
        And the browser's URL should contain "sex=male"
        And the browser's URL should contain "subscribe=subscribe"
        And the browser's URL should not contain "digest=digest"
        And the browser's URL should contain "countries=no"
        And the browser's URL should contain "countries=gr"
        And the browser's URL should contain "register=Register"
        And the browser's URL should contain "file=test.txt"
