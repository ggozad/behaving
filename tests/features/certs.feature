Feature: Self-signed certificates

    Scenario: Does not trigger errors when visiting sites with self-signed certs.
        Given Firefox as the default browser
        Given a browser
        When I visit "https://cacert.org"
        Then I should not see "Your connection is not private"

    Scenario: Does not trigger errors when visiting sites with self-signed certs.
        Given Chrome as the default browser
        Given a browser
        When I visit "https://cacert.org"
        Then I should not see "Your connection is not private"
