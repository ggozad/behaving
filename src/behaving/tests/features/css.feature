Feature: CSS steps
    @web
    Scenario: An invisible element isn't seen
        Given a browser
        When I visit "http://localhost:8080/css.html"
        Then the element with the css selector "#always-invisible" should not be visible

    @web
    Scenario: A single visible element is seen
        Given a browser
        When I visit "http://localhost:8080/css.html"
        Then the element with the css selector "#always-visible-div" should be visible

    @web
    Scenario: A hidden element is eventually seen after it becomes visible
        Given a browser
        When I visit "http://localhost:8080/css.html"
        Then the element with the css selector "#slowly-visible-div" should not be visible within 0 seconds
        But the element with the css selector "#slowly-visible-div" should be visible within 2 seconds

    @web
    Scenario: A visible element is eventually not seen after it becomes hidden
        Given a browser
        When I visit "http://localhost:8080/css.html"
        Then the element with the css selector "#slowly-invisible" should be visible within 0 seconds
        But the element with the css selector "#slowly-invisible" should not be visible within 2 seconds

    @web
    Scenario: An exact number of visible elements is seen
        Given a browser
        When I visit "http://localhost:8080/css.html"
        Then 3 elements with the css selector "#always-visible-list > li" should be visible

    @web
    Scenario: At least N visible elements are seen
        Given a browser
        When I visit "http://localhost:8080/css.html"
        Then at least 2 elements with the css selector "#always-visible-list > li" should be visible

    @web
    Scenario: An exact number of hidden elements are eventually seen after they become visible
        Given a browser
        When I visit "http://localhost:8080/css.html"
        Then the element with the css selector "#slowly-visible-list" should not be visible within 0 seconds
        But 3 elements with the css selector "#slowly-visible-list > li" should be visible within 2 seconds

    @web
    Scenario: At least N hidden elements are eventually seen after they become visible
        Given a browser
        When I visit "http://localhost:8080/css.html"
        Then the element with the css selector "#slowly-visible-list" should not be visible within 0 seconds
        But at least 2 elements with the css selector "#slowly-visible-list > li" should be visible within 2 seconds