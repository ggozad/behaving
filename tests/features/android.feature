Feature: Android emulator support

    Background:
        Given the android app at "android/app/build/outputs/apk/debug/app-debug.apk"
        Given Android as the default browser
        When I set the android capabilities to "{"deviceName": "rntest"}"

    @mobile
    Scenario: Element visibility
        Given a browser
        When I press "Visibility"
        Then I should see "Visibility mobile tests" within 2 seconds
        And I should not see "Inexistent text"
        And I should see an element with accessibility id "TouchableOpacity"

    @mobile
    Scenario: Pressing buttons and opacities
        Given a browser
        When I press "Touches"
        Then I should see "Touch mobile tests" within 2 seconds
        When I press "NORMAL BUTTON"
        Then I should see "Normal button pressed"
        When I press "TouchableOpacity"
        Then I should see "Touchable opacity pressed"
        When I press the element with xpath "(//android.widget.Button)[2]"
        Then I should see "Normal button pressed"
        When I tap at 360 600
        Then I should see "Tap at 38, 21.5"

    @mobile
    Scenario: Text inputs
        Given a browser
        When I press "Input"
        Then I should see "Input mobile tests" within 2 seconds
        When I fill in "Text Input" with "Testing 123..."
        Then I should see "You typed: Testing 123..."
        When I clear field "Text Input"
        Then I should not see "Testing 123..."
        When I fill in "Text Input" with "Testing 456..."
        Then I should see "You typed: Testing 456..."
        When I clear field "Prefilled Input"
        When I fill in "Prefilled Input" with "Testing prefilled..."
        Then I should see "You typed: Testing prefilled..."

    @mobile
    Scenario: TouchId/FaceId
        # To have this test pass on android you need to set up
        # the fingerprint on the emulator first.
        # Navigate to Settings/Security and start setting up fingerprints.
        # When requested to add a fingerprint run
        # adb -e emu finger touch 1
        # to simulate touches
        Given a browser
        And I press "Auth"
        Then I should see "TouchId/FaceId mobile tests" within 2 seconds
        When I press "Request TouchId"
        Then I should see "to test TouchId"
        When I match the TouchId fingerprint
        Then I should see "TouchId success"
        When I press "Request TouchId"
        Then I should see "to test TouchId"
        When I press "CANCEL"
        Then I should see "TouchId failure"
