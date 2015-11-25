Feature: CSS steps
    @web
    Scenario: An invisible element isn't seen
        Given a browser
        When I visit "http://localhost:8080/css.html"
        Then I should not see an element visible with the css selector "#always-invisible"

    @web
    Scenario: A single visible element is seen
        Given a browser
        When I visit "http://localhost:8080/css.html"
        Then I should see an element visible with the css selector "#always-visible-div"

    @web
    Scenario: A hidden element is eventually seen after it becomes visible
        Given a browser
        When I visit "http://localhost:8080/css.html"
        Then I should not see an element visible with the css selector "#slowly-visible-div" within 0 seconds
        But I should see an element visible with the css selector "#slowly-visible-div" within 2 seconds

    @web
    Scenario: A visible element is eventually not seen after it becomes hidden
        Given a browser
        When I visit "http://localhost:8080/css.html"
        Then I should see an element visible with the css selector "#slowly-invisible" within 0 seconds
        But I should not see an element visible with the css selector "#slowly-invisible" within 2 seconds

    @web
    Scenario: An exact number of visible elements is seen
        Given a browser
        When I visit "http://localhost:8080/css.html"
        Then I should see 3 elements visible with the css selector "#always-visible-list > li"

    @web
    Scenario: At least N visible elements are seen
        Given a browser
        When I visit "http://localhost:8080/css.html"
        Then I should see at least 2 elements visible with the css selector "#always-visible-list > li"

    @web
    Scenario: An exact number of hidden elements are eventually seen after they become visible
        Given a browser
        When I visit "http://localhost:8080/css.html"
        Then I should not see an element visible with the css selector "#slowly-visible-list" within 0 seconds
        But I should see 3 elements visible with the css selector "#slowly-visible-list > li" within 2 seconds

    @web
    Scenario: At least N hidden elements are eventually seen after they become visible
        Given a browser
        When I visit "http://localhost:8080/css.html"
        Then I should not see an element visible with the css selector "#slowly-visible-list" within 0 seconds
        But I should see at least 2 elements visible with the css selector "#slowly-visible-list > li" within 2 seconds