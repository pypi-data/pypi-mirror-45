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

As a user I try to submit the Contact-Form with a missing value
    When I navigate to the Contact-Form
    And I fill the form fields without checking the DSGVO compliance
    And I try submitting without checking the DSGVO compliance
    Then I should see an error message

As a user I try to submit the Contact-Form with all values
    When I navigate to the Contact-Form
    And I fill the form fields without checking the DSGVO compliance
    And I try submitting after checking the DSGVO compliance
    Then I should see a success message
