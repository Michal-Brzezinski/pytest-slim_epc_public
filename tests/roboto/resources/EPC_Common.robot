*** Settings ***
Resource          EPC_API.robot
Resource          EPC_Assertions.robot

*** Keywords ***
Reset EPC Should Succeed
    ${resp}=    Reset EPC
    Response Status Should Be    ${resp}    200

Prepare Clean EPC Environment
    [Documentation]    Backward-compatible alias for suite setup readability.
    Reset EPC Should Succeed

Attach UE To Network
    [Arguments]    ${ue_id}
    Attach UE    ${ue_id}

Attach The Default UE
    Attach UE To Network    ${UE_VALID}

Attach UE With ID ${ue_id}
    [Documentation]    Attaches a User Equipment (UE) to the network using the provided UE ID.
    Attach UE    ${ue_id}

Add Bearer With ID ${bearer_id} To UE With ID ${ue_id}
    [Documentation]    Adds a dedicated bearer with the specified bearer ID to the given UE.
    ${resp}=    Add Bearer    ${ue_id}    ${bearer_id}
