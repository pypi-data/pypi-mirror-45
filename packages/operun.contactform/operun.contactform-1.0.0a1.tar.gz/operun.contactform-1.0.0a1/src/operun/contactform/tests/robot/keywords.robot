*** Keywords ***

# SITE

I'm logged in as a '${ROLE}'
    Enable autologin as  ${ROLE}

I am logged in as site administrator
    Element should be visible  css=body.userrole-site-administrator

# ACTIONS

Fill text field
    [arguments]  ${field_label}   ${text}
    Input Text  xpath=//form//div/input[preceding-sibling::label[contains(text(), '${field_label}')]]  ${text}

I navigate to the site login
    Go To  ${PLONE_URL}/login_form
    Wait Until Element Is Visible  xpath=(//form[@id="login_form"])

I enter valid credentials
    Input Text  __ac_name  admin
    Input Text  __ac_password  secret
    Click Element  //input[@name="submit"]

I am logged in
    Wait until page contains  You are now logged in
    Page should contain  You are now logged in

# CONTACT-FORM

I navigate to the Contact-Form
    Go To  ${PLONE_URL}/contact
    Wait Until Element Is Visible  xpath=(//form[@id="contactform"])

I fill the form fields without checking the DSGVO compliance
    Input Text  firstname  Max
    Input Text  lastname  Mustermann
    Input Text  email  max.mustermann@example.com
    Input Text  subject  We ♥ Plone
    Input Text  message  Plone «ταБЬℓσ»: 1<2 & 4+1>3, is 100% awesome!

I try submitting without checking the DSGVO compliance
    Focus  //button[@name="form.buttons.submit"]
    Click Element  //button[@name="form.buttons.submit"]

I try submitting after checking the DSGVO compliance
    Focus  //button[@name="form.buttons.submit"]
    Select Checkbox  //input[@name="dsgvo"]
    Click Element  //button[@name="form.buttons.submit"]

I should see an error message
    Wait Until Element Is Visible  xpath=(//aside[@id="global_statusmessage"])
    Page should contain  Something went wrong, please check the input!

I should see a success message
    Wait Until Element Is Visible  xpath=(//div[@id="contactform-wrapper"])
    Page should contain  Your message was successfully sent.
