*** Settings ***
Documentation     Start traffic validation tests for EPC simulator
Resource          ../../resources/EPC_API.robot
Resource          ../../resources/EPC_Assertions.robot
Resource          ../../resources/EPC_Common.robot
Resource          ../../resources/EPC_Traffic.robot

*** Test Cases ***
01 Start Traffic With Valid Parameters
    [Documentation]    Verifies that traffic can be started with valid UE, bearer, protocol, and speed.
    [Tags]    traffic    start-traffic    positive
    # Arrange
    Prepare Clean EPC Environment
    Attach The Default UE

    # Act
    Start Traffic With Valid Parameters

    # Assert
    Verify Start Traffic Succeeds

    # Cleanup
    Stop Traffic On Default Bearer

02 Start Traffic With Speed Out Of Range
    [Documentation]    Verifies that traffic start fails when the speed is out of the allowed range.
    [Tags]    traffic    start-traffic    negative    invalid-speed
    # Arrange
    Prepare Clean EPC Environment
    Attach The Default UE

    # Act
    Start Traffic With Invalid Speed

    # Assert
    Verify Start Traffic Fails For Invalid Speed

03 Start Traffic With Inactive Bearer
    [Documentation]    Verifies that traffic start fails when the bearer is not active for the UE.
    [Tags]    traffic    start-traffic    negative    inactive-bearer
    # Arrange
    Prepare Clean EPC Environment
    Attach The Default UE

    # Act
    Start Traffic On Inactive Bearer

    # Assert
    Verify Start Traffic Fails For Inactive Bearer

04 Start Traffic With Invalid UE ID
    [Documentation]    Verifies that traffic start fails when the UE ID is invalid or not connected.
    [Tags]    traffic    start-traffic    negative    invalid-ue
    # Arrange
    Prepare Clean EPC Environment

    # Act
    Start Traffic With Invalid UE ID

    # Assert
    Verify Start Traffic Fails For Invalid UE ID

05 Start Traffic With UE Not Attached
    [Documentation]    Verifies that traffic start fails when a valid UE ID is not attached.
    [Tags]    traffic    start-traffic    negative    not-attached
    # Arrange
    Prepare Clean EPC Environment

    # Act
    Start Traffic With UE Not Attached

    # Assert
    Verify Start Traffic Fails For UE Not Attached

06 Start Traffic With Kbps Only
    [Documentation]    Verifies that traffic can start with a kbps-only payload as allowed by OpenAPI.
    [Tags]    traffic    start-traffic    negative    openapi    kbps
    # Arrange
    Prepare Clean EPC Environment
    Attach The Default UE

    # Act
    Start Traffic With Kbps Only

    # Assert
    Verify Start Traffic Succeeds For Kbps Only

07 Start Traffic With Bps Only
    [Documentation]    Verifies that traffic can start with a bps-only payload as allowed by OpenAPI.
    [Tags]    traffic    start-traffic    negative    openapi    bps
    # Arrange
    Prepare Clean EPC Environment
    Attach The Default UE

    # Act
    Start Traffic With Bps Only

    # Assert
    Verify Start Traffic Succeeds For Bps Only

08 Start Traffic With Unsupported Protocol Smtp
    [Documentation]    Verifies that traffic start rejects an unsupported protocol value (smtp).
    [Tags]    traffic    start-traffic    negative    invalid-protocol
    # Arrange
    Prepare Clean EPC Environment
    Attach The Default UE

    # Act
    Start Traffic With Unsupported Protocol    smtp

    # Assert
    Verify Start Traffic Fails For Unsupported Protocol

09 Start Traffic With Unsupported Protocol Icmp
    [Documentation]    Verifies that traffic start rejects an unsupported protocol value (icmp).
    [Tags]    traffic    start-traffic    negative    invalid-protocol
    # Arrange
    Prepare Clean EPC Environment
    Attach The Default UE

    # Act
    Start Traffic With Unsupported Protocol    icmp

    # Assert
    Verify Start Traffic Fails For Unsupported Protocol

10 Start Traffic With Protocol As List
    [Documentation]    Verifies that traffic start rejects a protocol value provided as a list.
    [Tags]    traffic    start-traffic    negative    invalid-protocol    type
    # Arrange
    Prepare Clean EPC Environment
    Attach The Default UE

    # Act
    Start Traffic With Protocol List

    # Assert
    Verify Start Traffic Fails For Protocol List

11 Start Traffic With Extra Field
    [Documentation]    Verifies that traffic start rejects payloads with unexpected fields.
    [Tags]    traffic    start-traffic    negative    validation    extra-field
    # Arrange
    Prepare Clean EPC Environment
    Attach The Default UE

    # Act
    Start Traffic With Extra Field

    # Assert
    Verify Start Traffic Fails For Extra Field

12 Start Traffic Exceeds UE Total Limit
    [Documentation]    Verifies that total traffic across bearers does not exceed 100 Mbps per UE.
    [Tags]    traffic    start-traffic    negative    ue-limit
    # Arrange
    Prepare Clean EPC Environment
    Attach The Default UE
    Add Additional Bearer For UE

    # Act
    Start Traffic On Default Bearer With Speed    80
    Start Traffic On Additional Bearer With Speed    80

    # Assert
    Verify Second Start Fails For UE Limit

    # Cleanup
    Stop Traffic    ${UE_VALID}    ${BEARER_DEFAULT}
    Stop Traffic    ${UE_VALID}    1


*** Keywords ***
Start Traffic With Valid Parameters
    ${resp}=    Start Traffic    ${UE_VALID}    ${BEARER_DEFAULT}    ${TRAFFIC_PROTOCOL}    ${TRAFFIC_VALID}
    Set Test Variable    ${START_TRAFFIC_VALID_RESPONSE}    ${resp}

Verify Start Traffic Succeeds
    ${expected_bps}=    Evaluate    int(${TRAFFIC_VALID}) * 1000000
    Response Status Should Be    ${START_TRAFFIC_VALID_RESPONSE}    200
    Response Should Contain Key    ${START_TRAFFIC_VALID_RESPONSE}    status
    Response JSON Field Should Be    ${START_TRAFFIC_VALID_RESPONSE}    ue_id    ${UE_VALID}
    Response JSON Field Should Be    ${START_TRAFFIC_VALID_RESPONSE}    bearer_id    ${BEARER_DEFAULT}
    Response JSON Field Should Be    ${START_TRAFFIC_VALID_RESPONSE}    target_bps    ${expected_bps}

Stop Traffic On Default Bearer
    Stop Traffic On Bearer    ${UE_VALID}    ${BEARER_DEFAULT}

Start Traffic With Invalid Speed
    ${resp}=    Start Traffic    ${UE_VALID}    ${BEARER_DEFAULT}    ${TRAFFIC_PROTOCOL}    ${TRAFFIC_INVALID}
    Set Test Variable    ${START_TRAFFIC_INVALID_SPEED_RESPONSE}    ${resp}

Verify Start Traffic Fails For Invalid Speed
    Response Status Should Be    ${START_TRAFFIC_INVALID_SPEED_RESPONSE}    422

Start Traffic On Inactive Bearer
    ${resp}=    Start Traffic    ${UE_VALID}    ${BEARER_VALID}    ${TRAFFIC_PROTOCOL}    ${TRAFFIC_VALID}
    Set Test Variable    ${START_TRAFFIC_INACTIVE_BEARER_RESPONSE}    ${resp}

Verify Start Traffic Fails For Inactive Bearer
    Response Status Should Be    ${START_TRAFFIC_INACTIVE_BEARER_RESPONSE}    422
    Response Should Contain Message    ${START_TRAFFIC_INACTIVE_BEARER_RESPONSE}    Bearer not found

Start Traffic With Invalid UE ID
    ${resp}=    Start Traffic    ${UE_INVALID}    ${BEARER_DEFAULT}    ${TRAFFIC_PROTOCOL}    ${TRAFFIC_VALID}
    Set Test Variable    ${START_TRAFFIC_INVALID_UE_RESPONSE}    ${resp}

Verify Start Traffic Fails For Invalid UE ID
    Response Status Should Be    ${START_TRAFFIC_INVALID_UE_RESPONSE}    422
    Response Should Contain Message    ${START_TRAFFIC_INVALID_UE_RESPONSE}    UE not found

Start Traffic With UE Not Attached
    ${resp}=    Start Traffic    ${UE_VALID}    ${BEARER_DEFAULT}    ${TRAFFIC_PROTOCOL}    ${TRAFFIC_VALID}
    Set Test Variable    ${START_TRAFFIC_NOT_ATTACHED_RESPONSE}    ${resp}

Verify Start Traffic Fails For UE Not Attached
    Response Status Should Be    ${START_TRAFFIC_NOT_ATTACHED_RESPONSE}    422
    Response Should Contain Message    ${START_TRAFFIC_NOT_ATTACHED_RESPONSE}    UE not found

Start Traffic With Kbps Only
    ${kbps}=    Set Variable    1500
    ${payload}=    Create Dictionary    protocol=${TRAFFIC_PROTOCOL}    kbps=${kbps}
    ${resp}=    POST    /ues/${UE_VALID}/bearers/${BEARER_DEFAULT}/traffic    ${payload}
    Set Test Variable    ${START_TRAFFIC_KBPS_RESPONSE}    ${resp}
    ${expected_bps}=    Evaluate    int(${kbps}) * 1000
    Set Test Variable    ${START_TRAFFIC_KBPS_EXPECTED_BPS}    ${expected_bps}

Verify Start Traffic Succeeds For Kbps Only
    Response Status Should Be    ${START_TRAFFIC_KBPS_RESPONSE}    200
    Response JSON Field Should Be    ${START_TRAFFIC_KBPS_RESPONSE}    ue_id    ${UE_VALID}
    Response JSON Field Should Be    ${START_TRAFFIC_KBPS_RESPONSE}    bearer_id    ${BEARER_DEFAULT}
    Response JSON Field Should Be    ${START_TRAFFIC_KBPS_RESPONSE}    target_bps    ${START_TRAFFIC_KBPS_EXPECTED_BPS}

Start Traffic With Bps Only
    ${bps}=    Set Variable    500000
    ${payload}=    Create Dictionary    protocol=udp    bps=${bps}
    ${resp}=    POST    /ues/${UE_VALID}/bearers/${BEARER_DEFAULT}/traffic    ${payload}
    Set Test Variable    ${START_TRAFFIC_BPS_RESPONSE}    ${resp}
    Set Test Variable    ${START_TRAFFIC_BPS_EXPECTED_BPS}    ${bps}

Verify Start Traffic Succeeds For Bps Only
    Response Status Should Be    ${START_TRAFFIC_BPS_RESPONSE}    200
    Response JSON Field Should Be    ${START_TRAFFIC_BPS_RESPONSE}    ue_id    ${UE_VALID}
    Response JSON Field Should Be    ${START_TRAFFIC_BPS_RESPONSE}    bearer_id    ${BEARER_DEFAULT}
    Response JSON Field Should Be    ${START_TRAFFIC_BPS_RESPONSE}    target_bps    ${START_TRAFFIC_BPS_EXPECTED_BPS}

Start Traffic With Unsupported Protocol
    [Arguments]    ${protocol}
    ${payload}=    Create Dictionary    protocol=${protocol}    Mbps=${TRAFFIC_VALID}
    ${resp}=    POST    /ues/${UE_VALID}/bearers/${BEARER_DEFAULT}/traffic    ${payload}
    Set Test Variable    ${START_TRAFFIC_UNSUPPORTED_PROTOCOL_RESPONSE}    ${resp}

Verify Start Traffic Fails For Unsupported Protocol
    Response Status Should Be    ${START_TRAFFIC_UNSUPPORTED_PROTOCOL_RESPONSE}    422

Start Traffic With Protocol List
    ${protocols}=    Evaluate    ["tcp", "udp", "icmp"]
    ${payload}=    Create Dictionary    protocol=${protocols}    Mbps=${TRAFFIC_VALID}
    ${resp}=    POST    /ues/${UE_VALID}/bearers/${BEARER_DEFAULT}/traffic    ${payload}
    Set Test Variable    ${START_TRAFFIC_PROTOCOL_LIST_RESPONSE}    ${resp}

Verify Start Traffic Fails For Protocol List
    Response Status Should Be    ${START_TRAFFIC_PROTOCOL_LIST_RESPONSE}    422

Start Traffic With Extra Field
    ${payload}=    Create Dictionary    protocol=tcp    Mbps=3    extra=kotek
    ${resp}=    POST    /ues/${UE_VALID}/bearers/${BEARER_DEFAULT}/traffic    ${payload}
    Set Test Variable    ${START_TRAFFIC_EXTRA_FIELD_RESPONSE}    ${resp}

Verify Start Traffic Fails For Extra Field
    Response Status Should Be    ${START_TRAFFIC_EXTRA_FIELD_RESPONSE}    422

Add Additional Bearer For UE
    ${resp}=    Add Bearer    ${UE_VALID}    1
    Response Status Should Be    ${resp}    200

Start Traffic On Default Bearer With Speed
    [Arguments]    ${mbps}
    ${resp}=    Start Traffic    ${UE_VALID}    ${BEARER_DEFAULT}    ${TRAFFIC_PROTOCOL}    ${mbps}
    Set Test Variable    ${START_TRAFFIC_DEFAULT_SPEED_RESPONSE}    ${resp}

Start Traffic On Additional Bearer With Speed
    [Arguments]    ${mbps}
    ${resp}=    Start Traffic    ${UE_VALID}    1    ${TRAFFIC_PROTOCOL}    ${mbps}
    Set Test Variable    ${START_TRAFFIC_ADDITIONAL_SPEED_RESPONSE}    ${resp}

Verify Second Start Fails For UE Limit
    Response Status Should Be    ${START_TRAFFIC_ADDITIONAL_SPEED_RESPONSE}    422

