*** Settings ***
Library          Collections

*** Keywords ***
Response Status Should Be
    [Arguments]    ${resp}    ${expected}
    Should Be Equal As Integers    ${resp.status_code}    ${expected}

Response Should Contain Key
    [Arguments]    ${resp}    ${key}
    Dictionary Should Contain Key   ${resp.json()}    ${key}

Response Should Contain Message
    [Arguments]    ${resp}    ${expected}
    Should Contain    ${resp.text}    ${expected}

Response JSON Field Should Be
    [Arguments]    ${resp}    ${key}    ${expected}
    ${payload}=    Set Variable    ${resp.json()}
    ${actual}=    Get From Dictionary    ${payload}    ${key}
    Should Be Equal As Strings    ${actual}    ${expected}

Response JSON Nested Object Field Should Be
    [Arguments]    ${resp}    ${outer_key}    ${inner_key}    ${leaf_key}    ${expected}
    ${payload}=    Set Variable    ${resp.json()}
    ${nested}=    Get From Dictionary    ${payload}    ${outer_key}
    ${inner_key}=    Convert To String    ${inner_key}
    ${inner_object}=    Get From Dictionary    ${nested}    ${inner_key}
    ${actual}=    Get From Dictionary    ${inner_object}    ${leaf_key}
    Should Be Equal As Strings    ${actual}    ${expected}

    
