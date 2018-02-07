Feature: Android emulator support

    Background:
        Given the android app at "android/app/build/outputs/apk/app-debug.apk"
        Given Android as the default browser
        When I set the android capabilities to "{"deviceName": "Nexus_5X_API_26"}"

    @mobile
    Scenario: Element visibility
        Given a browser
        Then I should see "Behaving mobile tests"
        And I should not see "Inexistent text"
        And I should see an element with accessibility id "TouchableOpacity"

    @mobile
    Scenario: Pressing buttons and opacities
        Given a browser
        When I press "NORMAL BUTTON"
        Then I should see "Normal button pressed"
        When I press "TouchableOpacity"
        Then I should see "Touchable opacity pressed"
        When I press the element with xpath "//android.widget.Button"
        Then I should see "Normal button pressed"
        When I tap at 0 500
        Then I should see "Tap at"

    @mobile
    Scenario: Text inputs
        Given a browser
        When I fill in "Text Input" with "Testing 123..."
        Then I should see "You typed: Testing 123..."
