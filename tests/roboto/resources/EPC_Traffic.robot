*** Settings ***
Resource          EPC_API.robot
Resource          EPC_Assertions.robot

*** Keywords ***
Start Traffic On Bearer
    [Arguments]    ${ue_id}    ${bearer_id}    ${protocol}    ${mbps}
    ${resp}=    Start Traffic    ${ue_id}    ${bearer_id}    ${protocol}    ${mbps}
    ${expected_bps}=    Evaluate    int(${mbps}) * 1000000
    Response Status Should Be    ${resp}    200
    Response Should Contain Key    ${resp}    status
    Response JSON Field Should Be    ${resp}    ue_id    ${ue_id}
    Response JSON Field Should Be    ${resp}    bearer_id    ${bearer_id}
    Response JSON Field Should Be    ${resp}    target_bps    ${expected_bps}

Stop Traffic On Bearer
    [Arguments]    ${ue_id}    ${bearer_id}
    ${resp}=    Stop Traffic    ${ue_id}    ${bearer_id}
    Response Status Should Be    ${resp}    200
    Response Should Contain Key    ${resp}    status
    Response JSON Field Should Be    ${resp}    ue_id    ${ue_id}
    Response JSON Field Should Be    ${resp}    bearer_id    ${bearer_id}

