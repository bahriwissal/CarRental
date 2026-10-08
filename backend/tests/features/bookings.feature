Feature: Booking a car
  As a customer
  I want to book a car for a date range
  So that it is reserved for me and I know the price up front

  Dates are written relative to today ("today+10") so the specs never go stale.
  A booking covers the nights from start_date up to (not including) end_date.

  Background:
    Given a car "Renault Clio" priced 50 per day

  @REQ-BKG-001
  Scenario: The price is the number of days times the daily price
    When "Jane" books "Renault Clio" from "today+10" to "today+13"
    Then the response status is 201
    And the booking total price is 150

  @REQ-BKG-002
  Scenario: A car cannot be booked twice for overlapping dates
    Given "Jane" has booked "Renault Clio" from "today+10" to "today+13"
    When "John" books "Renault Clio" from "today+12" to "today+15"
    Then the response status is 409
    And the error detail contains "already booked"

  @REQ-BKG-003
  Scenario: Back-to-back bookings are allowed
    Given "Jane" has booked "Renault Clio" from "today+10" to "today+13"
    When "John" books "Renault Clio" from "today+13" to "today+15"
    Then the response status is 201

  @REQ-BKG-004
  Scenario Outline: The end date must be after the start date
    When "Jane" books "Renault Clio" from "<start>" to "<end>"
    Then the response status is 422
    And the error detail contains "end_date must be after start_date"

    Examples:
      | start    | end      |
      | today+14 | today+10 |
      | today+10 | today+10 |

  @REQ-BKG-005
  Scenario: A car marked unavailable cannot be booked
    Given an unavailable car "Dacia Duster" priced 45 per day
    When "Jane" books "Dacia Duster" from "today+10" to "today+12"
    Then the response status is 409
    And the error detail contains "not available"

  @REQ-BKG-006
  Scenario: Booking a car that does not exist
    When "Jane" books car id 9999 from "today+10" to "today+12"
    Then the response status is 404
    And the error detail contains "Car not found"

  @REQ-BKG-007
  Scenario: The customer email must look like an email address
    When "Jane" with email "not-an-email" books "Renault Clio" from "today+10" to "today+12"
    Then the response status is 422

  @REQ-BKG-008
  Scenario: Cancelling a booking frees the dates
    Given "Jane" has booked "Renault Clio" from "today+10" to "today+13"
    When I cancel the last booking
    Then the response status is 204
    When "John" books "Renault Clio" from "today+10" to "today+13"
    Then the response status is 201

  @REQ-BKG-009
  Scenario: Bookings are listed in start-date order
    Given "Late" has booked "Renault Clio" from "today+20" to "today+22"
    And "Early" has booked "Renault Clio" from "today+5" to "today+7"
    When I list the bookings
    Then the booking customers are "Early, Late"
