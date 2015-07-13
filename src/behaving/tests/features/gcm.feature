Feature: Send a GCM Notification

    @gcm
    Scenario: Receive GCM notification
    	When I send a gcm message "{"to":"1234", "data": {"message": "få bar", "badge": [0,1,2]}}"
    	Then I should receive a gcm notification at "1234" containing "{'data': {'badge': [0,1,2]}}"
    	And I should receive a gcm notification at "1234" containing "{'data': {'message': u'få bar'}}"
