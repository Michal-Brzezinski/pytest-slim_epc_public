*** Settings ***
Documentation   Tests of adding bearers
Resource        ../../resources/EPC_Common.robot
Resource        keywords/EPC_Bearers_Keywords.robot

Test Teardown   Reset EPC

*** Test Cases ***

# --- Valid ---

01 Add bearer with valid UE ID and bearer ID
    [Documentation]    Verify that a new bearer can be added to an attached UE when valid UE ID and bearer ID are provided.
    [Tags]    bearer    add    positive

    # Arrange
    Attach UE With ID 1

    # Act
    Add Bearer With ID 2 To UE With ID 1 Response With OK

    # Assert
    UE With ID 1 Have Bearer With ID 2


02 Add bearer response contain correct IDs and status
    [Documentation]    Verify that the response from adding a bearer contains the correct UE ID, bearer ID and Status.
    [Tags]    bearer    add    positive    response

    # Arrange
    Attach UE With ID 1

    # Act + Assert
    Add Bearer With ID 2 To UE With ID 1 Response With Correct Values


03 Add bearer lower boundary ID
    [Documentation]    Verify adding a bearer with the lowest allowed ID (ID = 1).
    [Tags]    bearer    add    positive    boundary

    # Arrange
    Attach UE With ID 1

    # Act
    Add Bearer With ID 1 To UE With ID 1 Response With OK

    # Assert
    UE With ID 1 Have Bearer With ID 1


04 Add bearer upper boundary ID
    [Documentation]    Verify adding a bearer with the highest allowed ID bearers (ID = 8).
    [Tags]    bearer    add    positive    boundary

    # Arrange
    Attach UE With ID 1

    # Act
    Add Bearer With ID 8 To UE With ID 1 Response With OK

    # Assert
    UE With ID 1 Have Bearer With ID 8


05 Add all bearers in the allowed range
    [Documentation]     Verify adding all bearers in allowed range (without adding default one).
    [Tags]  bearer  add     positive    all-bearers

    # Arrange
    Attach UE With ID 1

    # Act
    Add All Bearers In Allowed Range To UE With ID 1

    # Assert
    UE With ID 1 Have Exacly 9 Bearers


# --- Invalid ---

06 Add bearer under boundary ID
    [Documentation]    Verify that attempting to add a bearer with an ID below the allowed range (ID = 0) returns an Unprocessable Entity error and the bearer is not added.
    [Tags]    bearer    add    negative    boundary    invalid-bearer

    # Arrange
    Attach UE With ID 1

    # Act
    Add Bearer With ID 0 To UE With ID 1 Response With Unprocessable Entity

    # Assert
    UE With ID 1 Do Not Have Bearer With ID 0


07 Add bearer above boundary ID
    [Documentation]    Verify that attempting to add a bearer with an ID above the allowed range (ID = 10) returns an Unprocessable Entity error and the bearer is not added.
    [Tags]    bearer    add    negative    boundary    invalid-bearer

    # Arrange
    Attach UE With ID 1

    # Act
    Add Bearer With ID 10 To UE With ID 1 Response With Unprocessable Entity

    # Assert
    UE With ID 1 Do Not Have Bearer With ID 10


08 Add bearer under boundary ID response contain correct error type
    [Documentation]    Verify that the validation error response for an ID below the minimum boundary contains the 'greater_than_equal' error type.
    [Tags]    bearer    add    negative    error-type    invalid-bearer

    # Arrange
    Attach UE With ID 1

    # Act + Assert
    Add Bearer With ID 0 To UE With ID 1 Response With Greater Than Equal Error Type


09 Add bearer above boundary ID response contain correct error type
    [Documentation]    Verify that the validation error response for an ID above the maximum boundary contains the 'less_than_equal' error type.
    [Tags]    bearer    add    negative    error-type    invalid-bearer

    # Arrange
    Attach UE With ID 1

    # Act + Assert
    Add Bearer With ID 10 To UE With ID 1 Response With Less Than Equal Error Type


10 Add existing bearer
    [Documentation]    Verify that attempting to add a bearer that has already been attached to the UE results in a Unprocessable Entity error.
    [Tags]    bearer    add    negative    duplicate

    # Arrange
    Attach UE With ID 1
    Add Bearer With ID 2 To UE With ID 1

    # Act + Assert
    Add Bearer With ID 2 To UE With ID 1 Response With Unprocessable Entity

    # Assert
    UE With ID 1 Have Exacly 2 Bearers


11 Add bearer to non-existing UE
    [Documentation]    Verify that attempting to add a bearer to a UE that has not been attached yet results in a Unprocessable Entity error.
    [Tags]    bearer    add    negative    invalid-ue

    # Arrange
    Reset EPC

    # Act + Assert
    Add Bearer With ID 2 To UE With ID 1 Response With Unprocessable Entity


12 Add bearer without ID
    [Documentation]    Verify that attempting to add a bearer without providing a bearer ID results in an Unprocessable Entity error.
    [Tags]    bearer    add    negative    missing-id

    # Arrange
    Attach UE With ID 1

    # Act + Assert
    Add Bearer Without ID To UE With ID 1 Response With Unprocessable Entity

    # Assert
    UE With ID 1 Have Exacly 1 Bearers


*** Keywords ***

Add Bearer With ID ${bearer_id} To UE With ID ${ue_id} Response With OK
    [Documentation]    Sends a request to add a bearer and asserts that the response status code is 200 (OK).
    Add Bearer Should Response With    200      ${ue_id}    ${bearer_id}

Add All Bearers In Allowed Range To UE With ID ${ue_id}
    [Documentation]    Add bearers with ID range from 1 to 8, to UE with given ID.
    FOR    ${id}    IN RANGE    1   9
        Add Bearer With ID ${id} To UE With ID ${ue_id}
    END

Add Bearer With ID ${bearer_id} To UE With ID ${ue_id} Response With Unprocessable Entity
    [Documentation]    Sends a request to add a bearer and asserts that the response status code is 422 (Unprocessable Entity).
    Add Bearer Should Response With    422      ${ue_id}    ${bearer_id}

Add Bearer Without ID To UE With ID ${ue_id} Response With Unprocessable Entity
    [Documentation]    Sends a request to add a bearer with an empty ID and asserts that the response status code is 422 (Unprocessable Entity).
    Add Bearer Should Response With    422      ${ue_id}    ''

Add Bearer With ID ${bearer_id} To UE With ID ${ue_id} Response With Correct Values
    [Documentation]    Adds a bearer and verifies that the JSON response fields match the expected UE ID, bearer ID, and status.
    ${add_resp}=       Add Bearer    ${ue_id}   ${bearer_id}
    Response JSON Field Should Be  ${add_resp}     ue_id     ${ue_id}
    Response JSON Field Should Be  ${add_resp}     bearer_id     ${bearer_id}
    Response JSON Field Should Be  ${add_resp}     status     bearer_added

Add Bearer With ID ${bearer_id} To UE With ID ${ue_id} Response With Greater Than Equal Error Type
    [Documentation]    Adds a bearer and verifies that the validation error type returned is 'greater_than_equal'.
    Add Bearer Should Response With Error Type   greater_than_equal      ${ue_id}    ${bearer_id}

Add Bearer With ID ${bearer_id} To UE With ID ${ue_id} Response With Less Than Equal Error Type
    [Documentation]    Adds a bearer and verifies that the validation error type returned is 'less_than_equal'.
    Add Bearer Should Response With Error Type   less_than_equal      ${ue_id}   ${bearer_id}