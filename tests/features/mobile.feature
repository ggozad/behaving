Feature: Mobile

    @mobile
    Scenario: Use the ios simulator
        Given an iOS simulator running "ios/build/Build/Products/Debug-iphonesimulator/rntest.app"
        Then I should see "Behaving mobile tests"
        When I press "Normal button"
        Then I should see "Normal button pressed"
        When I press "Touchable opacity"
        Then I should see "Touchable opacity pressed"
