Feature: Mobile

    @mobile
    Scenario: Use the ios simulator
        Given an iOS simulator running "ios/build/Build/Products/Debug-iphonesimulator/rntest.app"
        Then I should see "Welcome to React Native!"
