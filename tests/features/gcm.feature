Feature: Send a GCM Notification

    @gcm
    Scenario: Receive GCM notifications
    	When I send a gcm message "{"to":"1234", "data": {"foo": "få", "bar": [0,1,2]}}"
    	And I send a gcm message "{"to":"1234", "data": {"foo": "foo", "bar": {"qux": "qux"}}}"
			Then I should receive a gcm notification at "1234" containing "{'data': {'foo': u'få'}}"
			And I should receive a gcm notification at "1234" containing "{'data': {'bar': [0,1,2]}}"
	    	And I should receive a gcm notification at "1234" containing "{'data': {'foo': 'foo'}}"
    		And I should receive a gcm notification at "1234" containing "{'data': {'bar': {'qux': 'qux'}}}"
