*** Settings ***
Documentation     Traffic scenario for a single bearer with clear AAA structure
Library           Collections
Resource          ../../resources/EPC_API.robot
Resource          ../../resources/EPC_Assertions.robot
Resource          ../../resources/EPC_Common.robot
Resource          ../../resources/EPC_Traffic.robot

*** Test Cases ***
01 Start Traffic Without Protocol Should Be Allowed By Documentation
    [Documentation]    Verifies that traffic start should work without protocol because documentation does not require it.
    [Tags]    traffic    single-bearer    positive
    # Arrange
    Prepare Clean EPC Environment
    Attach The Default UE

    # Act
    Start Traffic On The Default Bearer Without Protocol

    # Assert
    Verify Start Traffic Without Protocol Should Succeed

02 UE Starts And Stops Traffic On The Default Bearer
    [Documentation]    Verifies a business scenario: the UE is attached, starts traffic, and then stops it.
    [Tags]    traffic    single-bearer    positive
    # Arrange
    Prepare Clean EPC Environment

    # Act
    Attach The Default UE
    Start Traffic On The Default Bearer

    # Assert
    Verify Traffic On The Default Bearer

    # Cleanup
    Stop Traffic On The Default Bearer

03 End traffic for single bearer
    [Documentation]    Verifies that stopping traffic results in zero throughput being reported.
    [Tags]    traffic    single-bearer    positive
    # Arrange
    Prepare Clean EPC Environment
    Attach The Default UE
    Start Traffic On The Default Bearer

    # Act
    Stop Traffic On The Default Bearer

    # Assert
    Verify Traffic Is Stopped On The Default Bearer

*** Keywords ***
Start Traffic On The Default Bearer Without Protocol
    ${body}=    Create Dictionary    Mbps=50
    ${resp}=    POST    /ues/${UE_VALID}/bearers/${BEARER_DEFAULT}/traffic    ${body}
    Set Test Variable    ${START_TRAFFIC_NO_PROTOCOL_RESPONSE}    ${resp}

Verify Start Traffic Without Protocol Should Succeed
    Response Status Should Be    ${START_TRAFFIC_NO_PROTOCOL_RESPONSE}    200
    Response Should Contain Key    ${START_TRAFFIC_NO_PROTOCOL_RESPONSE}    status
    Response JSON Field Should Be    ${START_TRAFFIC_NO_PROTOCOL_RESPONSE}    ue_id    ${UE_VALID}
    Response JSON Field Should Be    ${START_TRAFFIC_NO_PROTOCOL_RESPONSE}    bearer_id    ${BEARER_DEFAULT}

Start Traffic On The Default Bearer
    Start Traffic On Bearer    ${UE_VALID}    ${BEARER_DEFAULT}    tcp    50

Verify Traffic On The Default Bearer
    ${resp}=    Check Traffic    ${UE_VALID}    ${BEARER_DEFAULT}
    Response Status Should Be    ${resp}    200
    Response JSON Field Should Be    ${resp}    ue_id    ${UE_VALID}
    Response JSON Field Should Be    ${resp}    bearer_id    ${BEARER_DEFAULT}
    Response JSON Field Should Be    ${resp}    protocol    tcp
    Response Should Contain Key    ${resp}    tx_bps
    Response Should Contain Key    ${resp}    rx_bps
    Response Should Contain Key    ${resp}    duration

Stop Traffic On The Default Bearer
    Stop Traffic    ${UE_VALID}    ${BEARER_DEFAULT}

Verify Traffic Is Stopped On The Default Bearer
    ${resp}=    Check Traffic    ${UE_VALID}    ${BEARER_DEFAULT}
    Response Status Should Be    ${resp}    200
    Response JSON Field Should Be    ${resp}    tx_bps    0
    Response JSON Field Should Be    ${resp}    rx_bps    0
