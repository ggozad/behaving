Feature: Mobile devices

    @mobile
    Scenario: Select iOS Simulator
        Given an iOS simulator running "TestApp.app"
        Then I should see "Test Gesture"
        And I press "Test Gesture"
        And I press "OK"
        And I wait for 3 seconds
        And I tap "mapEl" and drag to "[(0,0), (100,0), (0,100)]"
        And I wait for 3600 seconds
