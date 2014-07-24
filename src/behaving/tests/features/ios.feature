Feature: iOS support

    @ios
    @mobile
    Scenario: Test features with iOS simulator
        Given an iOS simulator running "ios_test_app/build/Release-iphonesimulator/ios_test_app.app"
        Then I should see "Result"
        And I should see an element with id "resultLabel"
        When I fill in "textInput" with "42"
        And I press "Calculate"
        Then I should see "84"
        # When I press "toggleCalculate"

    @ios
    @mobile
    Scenario: Application is installed
        Given an iOS simulator running "ios_test_app/build/Release-iphonesimulator/ios_test_app.app"
        When I close the app
        And I launch the app
        And I lock the device for 3 seconds
        #Then the application "com.behaving.test.app.ios-test-app" is installed