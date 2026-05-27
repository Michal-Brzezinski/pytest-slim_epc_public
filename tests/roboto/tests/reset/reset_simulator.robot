*** Settings ***
Documentation    Tests verifying that resetting the EPC simulator clears all state and succeeds in both idle and active conditions.
Resource         ../../resources/EPC_Common.robot
# Should the keywords from the file above be moved to common

Test Teardown    Reset EPC


*** Test Cases ***


# --- Valid ---

01 Reset simulator from idle state
    [Documentation]    Verify that resetting the simulator when no UE is attached results in an empty UE list.
    [Tags]    reset    simulator    positive

    # Act
    Reset EPC

    # Assert
    Get All UEs Response Should Be Empty


02 Reset simulator from active state
    [Documentation]    Verify that resetting the simulator clears all UEs and bearers.
    [Tags]    reset    simulator    positive    cleanup

    # Arrange
    Attach UE With ID 1
    Add Bearer With ID 2 To UE With ID 1 Response With OK

    # Act
    Reset EPC

    # Assert
    Get All UEs Response Should Be Empty


03 Reset simulator removes all bearers for all UEs
    [Documentation]    Verify that resetting the simulator removes all UEs and their bearers.
    [Tags]    reset    simulator    integration    cleanup

    # Arrange
    Attach UE With ID 1
    Add Bearer With ID 2 To UE With ID 1 Response With OK

    # Act
    Reset EPC

    # Assert
    Get All UEs Response Should Be Empty


*** Keywords ***

    
Simulator Should Have No UEs
    ${resp}=    Get All UEs
    ${json}=    Set Variable    ${resp.json()}
    ${count}=    Get Length    ${json["ues"]}
    Should Be Equal As Integers    ${count}    0

Get All UEs Response Should Be Empty
    [Documentation]    Verifies that the UE list returned by the API is empty.
    ${resp}=    Get All UEs
    ${json}=    Set Variable    ${resp.json()}
    Should Be Equal As Integers    ${json["ues"].__len__()}    0