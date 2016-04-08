Feature: File downloading

    @web
    Scenario: File-downloading with chrome
        Given Chrome as the default browser
        Given a browser
        When I go to "https://github.com/ggozad/behaving"
        And I press "Download ZIP"
        Then the file "behaving-master.zip" should have been downloaded within 3 seconds

    @web
    Scenario: File-downloading with firefox
        Given Firefox as the default browser
        Given a browser
        When I go to "https://github.com/ggozad/behaving"
        And I press "Download ZIP"
        Then the file "behaving-master.zip" should have been downloaded within 3 seconds
