*** Settings ***
Documentation     Detach validation tests for EPC simulator
Resource          ../../resources/EPC_API.robot
Resource          ../../resources/EPC_Assertions.robot
Resource          ../../resources/EPC_Common.robot

*** Test Cases ***
01 Detach UE With Valid ID
    [Documentation]    Verifies that an attached UE can be detached successfully.
    [Tags]    connection    detach    positive
    # Arrange
    Prepare Clean EPC Environment
    Attach The Default UE

    # Act
    Detach UE With Valid ID

    # Assert
    Verify Detach Succeeds

02 Detach UE Not Connected
    [Documentation]    Verifies that detaching a UE that is not connected returns an error.
    [Tags]    connection    detach    negative
    # Arrange
    Prepare Clean EPC Environment

    # Act
    Detach UE That Is Not Connected

    # Assert
    Verify Detach Fails For Not Connected UE

03 Detach UE With Invalid ID
    [Documentation]    Verifies that detaching with an invalid UE identifier returns a validation error.
    [Tags]    connection    detach    negative    invalid-ue
    # Arrange
    Prepare Clean EPC Environment

    # Act
    Detach UE With Invalid ID

    # Assert
    Verify Detach Fails For Invalid UE ID

*** Keywords ***
Detach UE With Valid ID
    ${resp}=    Detach UE    ${UE_VALID}
    Set Test Variable    ${DETACH_VALID_RESPONSE}    ${resp}

Verify Detach Succeeds
    Response Status Should Be    ${DETACH_VALID_RESPONSE}    200
    Response Should Contain Key    ${DETACH_VALID_RESPONSE}    status
    Response JSON Field Should Be    ${DETACH_VALID_RESPONSE}    ue_id    ${UE_VALID}

Detach UE That Is Not Connected
    ${resp}=    Detach UE    ${UE_VALID}
    Set Test Variable    ${DETACH_NOT_CONNECTED_RESPONSE}    ${resp}

Verify Detach Fails For Not Connected UE
    Response Status Should Be    ${DETACH_NOT_CONNECTED_RESPONSE}    422
    Response Should Contain Message    ${DETACH_NOT_CONNECTED_RESPONSE}    UE not found

Detach UE With Invalid ID
    ${resp}=    Detach UE    ${UE_INVALID}
    Set Test Variable    ${DETACH_INVALID_RESPONSE}    ${resp}

Verify Detach Fails For Invalid UE ID
    Response Status Should Be    ${DETACH_INVALID_RESPONSE}    422
