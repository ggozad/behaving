Feature: Frames
    @web
    Scenario: It can switch to a frame located using CSS
        Given a browser
        When I visit "http://localhost:8080/frame-page.html"
        Then I should not see "I'm the frame content"
        But I should see "I'm the page containing a frame"
        
        When I switch to frame with css "#my-frame"
        Then I should see "I'm the frame content"
        But I should not see "I'm the page containing a frame"

    @web
    Scenario: It can switch back to the main page
        Given a browser
        When I visit "http://localhost:8080/frame-page.html"
        Then I should not see "I'm the frame content"
        But I should see "I'm the page containing a frame"
        
        When I switch to frame with css "#my-frame"
        Then I should see "I'm the frame content"
        But I should not see "I'm the page containing a frame"

        When I switch back to the main page
        Then I should not see "I'm the frame content"
        But I should see "I'm the page containing a frame"