@no_remote_webdriver
Feature: File downloading

    @web
    Scenario: Check file download and contents with chrome
        Given Chrome as the default browser
        Given a browser
        When I go to "http://web/files.html"
        And I press "(testfile)"
        Then the file "test.txt" containing "Hello world" should have been downloaded within 3 seconds

    @web
    Scenario: Check file download with chrome
        Given Chrome as the default browser
        Given a browser
        When I go to "http://web/files.html"
        And I press "(testfile)"
        Then the file "test.txt" should have been downloaded within 3 seconds

    @web
    Scenario: Check file download with firefox
        Given Firefox as the default browser
        Given a browser
        When I go to "http://web/files.html"
        And I press "(testfile)"
        Then the file "test.txt" should have been downloaded within 3 seconds
