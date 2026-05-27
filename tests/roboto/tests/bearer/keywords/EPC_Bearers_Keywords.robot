*** Settings ***
Resource          ../../../resources/EPC_API.robot
Resource          ../../../resources/EPC_Assertions.robot

*** Keywords ***


# --- Remove bearer ---

Delete Bearer With ID ${bearer_id} From UE With ID ${ue_id} Response With Unprocessable Entity
    [Documentation]    Attempts to delete a bearer from the UE and verifies that the response status code is 422 (Unprocessable Entity).
    Delete Bearer Should Response With    422   ${ue_id}    ${bearer_id}


# --- UE (do not) have bearer ---

UE With ID ${ue_id} Have Bearer With ID ${bearer_id}
    [Documentation]    Verifies that the specified UE currently has the given bearer ID in its list of active bearers.
    ${resp}=    Get UE    ${ue_id}

    ${json_body}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Key    ${json_body}    bearers

    ${bearers}=    Get From Dictionary    ${json_body}    bearers
    ${bearer_id_str}=    Convert To String    ${bearer_id}
    Dictionary Should Contain Key    ${bearers}    ${bearer_id_str}

UE With ID ${ue_id} Do Not Have Bearer With ID ${bearer_id}
    [Documentation]    Verifies that the specified UE does not have the given bearer ID in its list of active bearers.
    ${resp}=    Get UE    ${ue_id}

    ${json_body}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Key    ${json_body}    bearers

    ${bearers}=    Get From Dictionary    ${json_body}    bearers
    ${bearer_id_str}=    Convert To String    ${bearer_id}
    Dictionary Should Not Contain Key    ${bearers}    ${bearer_id_str}

UE With ID ${ue_id} Have Exacly ${bearers_count} Bearers
    ${resp}=    Get UE    ${ue_id}

    ${json_body}=    Set Variable    ${resp.json()}
    ${bearers}=    Get From Dictionary    ${json_body}    bearers
    ${count}=    Get Length    ${bearers}

    Should Be Equal As Integers    ${count}    ${bearers_count}


# --- Utils ---

Add Bearer Should Response With
    [Documentation]    Adds a bearer to the UE and asserts that the HTTP response status code matches the expected value.
    [Arguments]    ${expected_status}   ${ue_id}    ${bearer_id}
    ${resp}=    Add Bearer    ${ue_id}    ${bearer_id}
    Should Be Equal As Integers    ${resp.status_code}    ${expected_status}

Add Bearer Should Response With Error Type
    [Documentation]    Adds a bearer and verifies that the validation error response contains the expected error type in its details.
    [Arguments]    ${expected_error_type}   ${ue_id}    ${bearer_id}
    ${resp}=    Add Bearer    ${ue_id}    ${bearer_id}
    ${json}=    Set Variable    ${resp.json()}
    ${actual_type}=    Set Variable    ${json["detail"][0]["type"]}
    Should Be Equal As Strings    ${actual_type}    ${expected_error_type}

Delete Bearer Should Response With
    [Documentation]    Deletes a bearer from the UE and asserts that the HTTP response status code matches the expected value.
    [Arguments]    ${expected_status}   ${ue_id}    ${bearer_id}
    ${resp}=    Delete Bearer    ${ue_id}    ${bearer_id}
    Should Be Equal As Integers    ${resp.status_code}    ${expected_status}