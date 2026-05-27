*** Settings ***
Library    EpcRequests.py
Resource   EPC_Variables.robot

*** Keywords ***

GET
    [Documentation]    Sends a GET request to the EPC API.
    [Arguments]    ${endpoint}
    ${resp}=    Request    GET    ${BASE_URL}${endpoint}    ${None}
    RETURN    ${resp}

POST
    [Documentation]    Sends a POST request to the EPC API with a JSON body.
    [Arguments]    ${endpoint}    ${body}
    ${resp}=    Request    POST    ${BASE_URL}${endpoint}    ${body}
    RETURN    ${resp}

DELETE
    [Documentation]    Sends a DELETE request to the EPC API.
    [Arguments]    ${endpoint}
    ${resp}=    Request    DELETE    ${BASE_URL}${endpoint}    ${None}
    RETURN    ${resp}


# --- EPC SPECIFIC KEYWORDS ---

Attach UE
    [Documentation]    Attaches a UE to the EPC simulator.
    [Arguments]    ${ue_id}
    ${body}=    Create Dictionary    ue_id=${ue_id}
    ${resp}=    POST    /ues    ${body}
    RETURN    ${resp}

Detach UE
    [Documentation]    Detaches a UE from the EPC simulator.
    [Arguments]    ${ue_id}
    ${resp}=    DELETE    /ues/${ue_id}
    RETURN    ${resp}

Get UE
    [Documentation]    Retrieves information about a specific UE.
    [Arguments]    ${ue_id}
    ${resp}=    GET    /ues/${ue_id}
    RETURN    ${resp}

Get All UEs
    [Documentation]    Returns a list of all UEs currently registered in the EPC simulator.
    ${resp}=    GET    /ues
    RETURN    ${resp}

Add Bearer
    [Documentation]    Adds a bearer to a UE.
    [Arguments]    ${ue_id}    ${bearer_id}
    ${body}=    Create Dictionary    bearer_id=${bearer_id}
    ${resp}=    POST    /ues/${ue_id}/bearers    ${body}
    RETURN    ${resp}

Delete Bearer
    [Documentation]    Deletes a bearer from a UE.
    [Arguments]    ${ue_id}    ${bearer_id}
    ${resp}=    DELETE    /ues/${ue_id}/bearers/${bearer_id}
    RETURN    ${resp}

Start Traffic
    [Documentation]    Starts traffic on a specific bearer.
    [Arguments]    ${ue_id}    ${bearer_id}    ${protocol}    ${Mbps}
    ${body}=    Create Dictionary    protocol=${protocol}    Mbps=${Mbps}
    ${resp}=    POST    /ues/${ue_id}/bearers/${bearer_id}/traffic    ${body}
    RETURN    ${resp}

Stop Traffic
    [Documentation]    Stops traffic on a specific bearer.
    [Arguments]    ${ue_id}    ${bearer_id}
    ${resp}=    DELETE    /ues/${ue_id}/bearers/${bearer_id}/traffic
    RETURN    ${resp}

Check Traffic
    [Documentation]    Retrieves current traffic statistics for a bearer.
    [Arguments]    ${ue_id}    ${bearer_id}
    ${resp}=    GET    /ues/${ue_id}/bearers/${bearer_id}/traffic
    RETURN    ${resp}

Reset EPC
    [Documentation]    Resets the entire EPC simulator, clearing all UEs and bearers.
    ${resp}=    POST    /reset    ${None}
    RETURN    ${resp}