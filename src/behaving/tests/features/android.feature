Feature: Android support

    @android
    @mobile
    Scenario: Test basic/form features with Android simulator
        Given "foo" as the persona
        Given I set "p" to "com.behaving.test.app.android_test_app"
        Given an Android simulator running "android_test_app/build/outputs/apk/android_test_app-release-unsigned.apk"
        Then I should see "Result"
        And I should see an element with id "$p:id/scrollView1"
        And I should not see an element with id "nonExistent"
        And I should see an element with xpath "//android.widget.TextView"
        And I should not see an element with xpath "//NonExistent"
        When I fill in "$p:id/textInput" with "42"
        And I press "Calculate"
        Then I should see "84.0"
        When I clear field "$p:id/textInput"
        Then I should not see "42"
        When I check "$p:id/switch1"
        Then attribute "checked" of field "$p:id/switch1" should have the value "true"
        When I uncheck "$p:id/switch1"
        Then attribute "checked" of field "$p:id/switch1" should have the value "false"
        # Slider set_value not implemented on appium for android
        # When I slide "$p:id/seekBar1" to 20%
        # Then field "$p:id/seekBar1" should have the value "20%"

    @android
    @mobile
    Scenario: Test tag & drag
        # Not working on android
        # Given "foo" as the persona
        # Given I set "p" to "com.behaving.test.app.android_test_app"
        # Given an Android simulator running "android_test_app/build/outputs/apk/android_test_app-release-unsigned.apk"
        # When I tap "$p:id/seekBar1" and drag to "[(50,0)]"
        # And I wait for 20 seconds
        # Then field "$p:id/seekBar1" should have the value "100%"

    @android
    @mobile
    Scenario: Close launch app
        Given an Android simulator running "android_test_app/build/outputs/apk/android_test_app-release-unsigned.apk"
        When I close the app
        And I launch the app
        Then I should see "Result"
        # Locking not implemented on android
        #And I lock the device
        #Then I should not see "Result"

    @persona
    @android
    @mobile
    Scenario: Save/load files from device
        Given "foo" as the persona
        Given an Android simulator running "android_test_app/build/outputs/apk/android_test_app-release-unsigned.apk"
        When I push the file "test.txt" to the device at "/data/local/tmp/test.txt"
        And I pull the file "/data/local/tmp/test.txt" from the app and set it to "foo"
        Then "foo" is set to "Hello world"
        Then I pull the file "/data/local/tmp/test.txt" from the app and save it to "/tmp/test.txt"
