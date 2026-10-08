Feature: Car fleet management
  As a rental agency
  I want to manage the cars in my fleet
  So that customers only see cars they can actually rent

  @REQ-SYS-001
  Scenario: The API reports that it is healthy
    When I GET "/api/health"
    Then the response status is 200
    And the response field "status" is "ok"

  @REQ-CAR-001
  Scenario: List every car in the fleet
    Given a car "Renault Clio" priced 35 per day
    And a car "Peugeot 208" priced 40 per day
    When I list the cars
    Then the response status is 200
    And the car list is exactly "Renault Clio, Peugeot 208"

  @REQ-CAR-002
  Scenario: Filter the list to cars available for rent
    Given a car "Renault Clio" priced 35 per day
    And an unavailable car "Dacia Duster" priced 45 per day
    When I list the cars with available "true"
    Then the car list is exactly "Renault Clio"

  @REQ-CAR-003
  Scenario: Add a car to the fleet
    When I create a car "Toyota Corolla" from 2023 priced 55 per day
    Then the response status is 201
    And the response has an "id"
    And the response field "available" is true

  @REQ-CAR-004
  Scenario Outline: Reject a car with invalid data
    When I create a car "Toyota Corolla" from <year> priced <price> per day
    Then the response status is 422

    Examples:
      | year | price |
      | 1989 | 55    |
      | 2023 | 0     |
      | 2023 | -10   |

  @REQ-CAR-005
  Scenario: Update only the fields that were sent
    Given a car "Renault Clio" priced 35 per day
    When I update car "Renault Clio" with daily price 42
    Then the response status is 200
    And the response field "daily_price" is 42
    And the response field "model" is "Clio"

  @REQ-CAR-006
  Scenario: Remove a car from the fleet
    Given a car "Renault Clio" priced 35 per day
    When I delete car "Renault Clio"
    Then the response status is 204
    And car "Renault Clio" no longer exists

  @REQ-CAR-007
  Scenario: Asking for a car that does not exist
    When I GET "/api/cars/9999"
    Then the response status is 404
    And the error detail contains "Car not found"
