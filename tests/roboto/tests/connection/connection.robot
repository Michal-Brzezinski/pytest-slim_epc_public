*** Settings ***
Documentation     Basic connectivity and attach validation tests for EPC simulator
Resource          ../../resources/EPC_API.robot
Resource          ../../resources/EPC_Assertions.robot
Resource          ../../resources/EPC_Common.robot

*** Test Cases ***
01 EPC Root Should Respond
    [Tags]    connection    smoke    positive
    ${resp}=    GET    /
    Response Status Should Be    ${resp}    200

02 Attach Same UE Twice Should Fail
    [Documentation]    Verifies duplicate attach is rejected for the same UE identifier.
    [Tags]    connection    negative    duplicate-attach
    # Arrange
    Prepare Clean EPC Environment

    # Act
    Attach UE First Time
    Attach Same UE Second Time

    # Assert
    Verify First Attach Succeeds
    Verify Second Attach Fails As Duplicate

03 Attach UE With ID 0
    [Documentation]    Verifies attach with ue_id=0 according to documentation range 0-100.
    [Tags]    connection    documentation-gap    attach-zero
    # Arrange
    Prepare Clean EPC Environment

    # Act
    Attach UE With Zero ID

    # Assert
    Verify Attach With Zero ID Should Succeed

*** Keywords ***
Attach UE First Time
    ${resp}=    Attach UE    ${UE_VALID}
    Set Test Variable    ${FIRST_ATTACH_RESPONSE}    ${resp}

Attach Same UE Second Time
    ${resp}=    Attach UE    ${UE_VALID}
    Set Test Variable    ${SECOND_ATTACH_RESPONSE}    ${resp}

Verify First Attach Succeeds
    Response Status Should Be    ${FIRST_ATTACH_RESPONSE}    200
    Response Should Contain Key    ${FIRST_ATTACH_RESPONSE}    status
    Response JSON Field Should Be    ${FIRST_ATTACH_RESPONSE}    ue_id    ${UE_VALID}

Verify Second Attach Fails As Duplicate
    Response Status Should Be    ${SECOND_ATTACH_RESPONSE}    400
    Response Should Contain Message    ${SECOND_ATTACH_RESPONSE}    already

Attach UE With Zero ID
    ${resp}=    Attach UE    0
    Set Test Variable    ${ZERO_ATTACH_RESPONSE}    ${resp}

Verify Attach With Zero ID Should Succeed
    Response Status Should Be    ${ZERO_ATTACH_RESPONSE}    200
    Response Should Contain Key    ${ZERO_ATTACH_RESPONSE}    status
    Response JSON Field Should Be    ${ZERO_ATTACH_RESPONSE}    ue_id    0

