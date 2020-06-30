Feature: File downloading

    @web
    Scenario: Check file download and contents with chrome
        Given Chrome as the default browser
        Given a browser
        When I go to "https://github.com/ggozad/behaving/releases"
        And I press "zip"
        Then the file "behaving-2.0.0.zip" containing "behaving" should have been downloaded within 3 seconds

    @web
    Scenario: Check file download with chrome
        Given Chrome as the default browser
        Given a browser
        When I go to "https://github.com/ggozad/behaving/releases"
        And I press "zip"
        Then the file "behaving-2.0.0.zip" should have been downloaded within 3 seconds

    @web
    Scenario: Check file download with firefox
        Given Firefox as the default browser
        Given a browser
        When I go to "https://github.com/ggozad/behaving/releases"
        And I press "zip"
        Then the file "behaving-2.0.0.zip" should have been downloaded within 3 seconds
