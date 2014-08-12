Feature: iOS support

    @ios
    @mobile
    Scenario: Test features with iOS simulator
        Given an iOS simulator running "ios_test_app/build/Release-iphonesimulator/ios_test_app.app"
        Then I should see "Result"
        And I should see an element with id "resultLabel"
        And I should not see an element with id "nonExistent"
        And I should see an element with xpath "//UIAStaticText"
        And I should not see an element with xpath "//NonExistent"
        When I fill in "textInput" with "42"
        And I press "Calculate"
        Then I should see "84"

    @ios
    @mobile
    Scenario: Close launch app
        Given an iOS simulator running "ios_test_app/build/Release-iphonesimulator/ios_test_app.app"
        When I close the app
        And I launch the app
        Then I should see "Result"
        And I lock the device
        Then I should not see "Result"

    @persona
    @ios
    @mobile
    Scenario: Save/load files from device
        Given "Foo" as the persona
        Given an iOS simulator running "ios_test_app/build/Release-iphonesimulator/ios_test_app.app"
        When I push the file "test.txt" to the device at "/ios_test_app.app/../Documents/test.txt"
        And I pull the file "/ios_test_app.app/../Documents/test.txt" from the app and set it to "foo"
        Then "foo" is set to "Hello world"
        Then I pull the file "/ios_test_app.app/../Documents/test.txt" from the app and save it to "/tmp/test.txt"

    @ios
    @mobile
    Scenario: Dirty iOS simulator
        Given a dirty iOS simulator running "ios_test_app/build/Release-iphonesimulator/ios_test_app.app"
        Then I should see "Result:" within 10 seconds
        And I should see an element with id "textInput"
        Then I fill in "textInput" with "42"
        When I restart the iOS simulator
        Then field "textInput" should have the value "42"
