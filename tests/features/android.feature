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
