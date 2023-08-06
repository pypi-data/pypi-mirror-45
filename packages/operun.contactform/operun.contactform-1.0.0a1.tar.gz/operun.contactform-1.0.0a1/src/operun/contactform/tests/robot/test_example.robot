*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  DebugLibrary

Variables  variables.py

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Test Cases ***

As a member I want to be able to log into the website
    [Documentation]  Example of a BDD-style (Behavior-driven development) test.
    When I navigate to the site login
    And I enter valid credentials
    Then I am logged in
