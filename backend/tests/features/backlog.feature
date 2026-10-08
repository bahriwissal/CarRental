@backlog
Feature: Backlog (specified, not implemented yet)
  These requirements are agreed but the code does not satisfy them yet.
  They are skipped by `make test` and run with `make test-backlog` or `make req ID=...`.
  Once one is implemented, move its scenario into the matching feature file and drop it from here.

  Background:
    Given a car "Renault Clio" priced 50 per day

  @REQ-BKG-010
  Scenario: A booking cannot start in the past
    When "Jane" books "Renault Clio" from "today-1" to "today+2"
    Then the response status is 422
    And the error detail contains "start_date cannot be in the past"

  @REQ-BKG-011
  Scenario: Fetch a single booking by id
    Given "Jane" has booked "Renault Clio" from "today+10" to "today+13"
    When I fetch the last booking
    Then the response status is 200
    And the response field "customer_name" is "Jane"
    When I GET "/api/bookings/9999"
    Then the response status is 404
    And the error detail contains "Booking not found"

  @REQ-BKG-012
  Scenario: Filter bookings by car
    Given a car "Peugeot 208" priced 40 per day
    And "Jane" has booked "Renault Clio" from "today+10" to "today+13"
    And "John" has booked "Peugeot 208" from "today+10" to "today+13"
    When I list the bookings for car "Peugeot 208"
    Then the booking customers are "John"
