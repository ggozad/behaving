Feature: Mobile

    Background:
        Given an iOS simulator running "ios/build/Build/Products/Debug-iphonesimulator/rntest.app"


    @mobile
    Scenario: Pressing buttons and opacities
        Then I should see "Behaving mobile tests"
        And I should not see "Inexistent text"
        And I should see an element with accessibility id "Touchable opacity"

    @mobile
    Scenario: Pressing buttons and opacities
        When I press "Normal button"
        Then I should see "Normal button pressed"
        When I press "Touchable opacity"
        Then I should see "Touchable opacity pressed"

    @mobile
    Scenario: Text inputs
        When I fill in "Text Input" with "Testing 123..."
        Then I should see "You typed: Testing 123..."