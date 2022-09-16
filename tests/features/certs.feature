Feature: Self-signed certificates

    @web
    Scenario: Does not trigger errors when visiting sites with self-signed certs.
        Given Firefox as the default browser
        Given a browser
        When I visit "https://cacert.org"
        Then I should not see "Your connection is not private"

    @web
    Scenario: Does not trigger errors when visiting sites with self-signed certs.
        Given Chrome as the default browser
        Given a browser
        When I visit "https://cacert.org"
        Then I should not see "Your connection is not private"

    @web
    Scenario: Access a local self-signed certificate
        Given Chrome as the default browser
        Given a browser
        When I visit "https://web"
        Then I should see "Hello world"

    @web
    Scenario: Access a local self-signed certificate
        Given Firefox as the default browser
        Given a browser
        When I visit "https://web"
        Then I should see "Hello world"
