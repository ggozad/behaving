Feature: iOS support

    @android
    @mobile
    Scenario: Test features with Android simulator
        Given "Leland" as the persona
        Given I set "p" to "com.behaving.test.app.android_test_app"
        Given an Android simulator running "android_test_app/bin/android_test_app.apk"
        Then I should see "Result"
        And I should see an element with id "$p:id/scrollView1"
        And I should not see an element with id "nonExistant"
        And I should see an element with xpath "//android.widget.TextView"
        And I should not see an element with xpath "//NonExistant"
        When I fill in "$p:id/textInput" with "42"
        And I press "Calculate"
        Then I should see "84.0"

