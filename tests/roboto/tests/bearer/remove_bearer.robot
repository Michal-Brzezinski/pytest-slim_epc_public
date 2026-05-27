*** Settings ***
Documentation   Tests of removing bearers
Resource        ../../resources/EPC_Common.robot
Resource        keywords/EPC_Bearers_Keywords.robot

Test Teardown   Reset EPC

*** Test Cases ***

# --- Valid ---

01 Delete correct bearer valid UE ID and Bearer ID
    [Documentation]    Verify successful deletion of a previously added dedicated bearer.
    [Tags]    bearer    remove    positive

    # Arrange
    Attach UE With ID 1
    Add Bearer With ID 2 To UE With ID 1

    # Act
    Delete Bearer With ID 2 From UE With ID 1 Response With OK

    # Assert
    UE With ID 1 Do Not Have Bearer With ID 2


02 Delete bearer contain correct IDs and status
    [Documentation]    Verify that the response from deleting a bearer contains the correct UE ID, Bearer ID and Status.
    [Tags]    bearer    remove    positive    response

    # Arrange
    Attach UE With ID 1
    Add Bearer With ID 2 To UE With ID 1

    # Act + Assert
    Delete Bearer With ID 2 From UE With ID 1 Response With Correct Values


# --- Invalid ---

03 Delete non-existing bearer
    [Documentation]    Verify that attempting to delete a bearer that has not been attached to the UE results in a Unprocessable Entity error and don't remove any other bearer.
    [Tags]    bearer    remove    negative    invalid-bearer

    # Arrange
    Attach UE With ID 1

    # Act + Assert
    Delete Bearer With ID 5 From UE With ID 1 Response With Unprocessable Entity

    # Assert
    UE With ID 1 Have Exacly 1 Bearers


04 Delete bearer under boundary ID
    [Documentation]    Verify that attempting to delete a bearer with an ID below the allowed range (ID = 0) returns an Unprocessable Entity error and don't remove any other bearer.
    [Tags]    bearer    remove    negative    missing-id

    # Arrange
    Attach UE With ID 1

    # Act + Assert
    Delete Bearer With ID 0 From UE With ID 1 Response With Unprocessable Entity

    # Assert
    UE With ID 1 Have Exacly 1 Bearers


05 Delete bearer above boundary ID
    [Documentation]    Verify that attempting to delete a bearer with an ID above the allowed range (ID = 10) returns an Unprocessable Entity error and don't remove any other bearer.
    [Tags]    bearer    remove    negative    missing-id

    # Arrange
    Attach UE With ID 1

    # Act + Assert
    Delete Bearer With ID 10 From UE With ID 1 Response With Unprocessable Entity

    # Assert
    UE With ID 1 Have Exacly 1 Bearers


06 Delete bearer without ID
    [Documentation]    Verify that attempting to delete a bearer without providing a bearer ID results in an Unprocessable Entity error and don't remove any other bearer
    [Tags]    bearer    remove    negative    missing-id

    # Arrange
    Attach UE With ID 1

    # Act + Assert
    Delete Bearer Without ID From UE With ID 1 Response With Unprocessable Entity

    # Assert
    UE With ID 1 Have Exacly 1 Bearers


*** Keywords ***

Delete Bearer With ID ${bearer_id} From UE With ID ${ue_id} Response With OK
    [Documentation]    Sends a request to delete a bearer from the UE and asserts that the response status code is 200 (OK).
    Delete Bearer Should Response With    200   ${ue_id}    ${bearer_id}

Delete Bearer Without ID From UE With ID ${ue_id} Response With Unprocessable Entity
    [Documentation]    Sends a request to delete a bearer with an empty ID and asserts that the response status code is 422 (Unprocessable Entity).
    Delete Bearer Should Response With    422   ${ue_id}    ''

Delete Bearer With ID ${bearer_id} From UE With ID ${ue_id} Response With Correct Values
    [Documentation]    Deletes a bearer from the UE and verifies that the JSON response fields match the expected UE ID, bearer ID, and status indicating successful deletion.
    ${add_resp}=       Delete Bearer    ${ue_id}   ${bearer_id}
    Response JSON Field Should Be  ${add_resp}     ue_id     ${ue_id}
    Response JSON Field Should Be  ${add_resp}     bearer_id     ${bearer_id}
    Response JSON Field Should Be  ${add_resp}     status     bearer_deleted
