*** Settings ***
Library    SSHLibrary

*** Variables ***
${ADMIN_USER}    admin
${ADMIN_PASSWORD}    Nethesis,1234
${module_id}    ${EMPTY}
${ZONE}    robot.example

*** Keywords ***
Login to cluster-admin
    New Page    https://${NODE_ADDR}/cluster-admin/
    Fill Text    text="Username"    ${ADMIN_USER}
    Click    button >> text="Continue"
    Fill Text    text="Password"    ${ADMIN_PASSWORD}
    Click    button >> text="Log in"
    Wait For Elements State    css=#main-content    visible    timeout=10s

Run action
    [Arguments]    ${action}    ${data}={}
    ${output}  ${rc} =    Execute Command    api-cli run module/${module_id}/${action} --data '${data}'
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    ${parsed} =    Evaluate    json.loads(r'''${output}''' or '{}')    modules=json
    RETURN    ${parsed}

Refused action
    [Arguments]    ${action}    ${data}    ${code}
    ${output}  ${stderr}  ${rc} =    Execute Command    api-cli run module/${module_id}/${action} --data '${data}'
    ...    return_rc=True    return_stderr=True
    Should Not Be Equal As Integers    ${rc}  0
    Should Contain    ${output}${stderr}    ${code}

Serial on the VPN address
    # Asks the running server over DNS, with the module's own stub resolver
    ${vpn} =    Execute Command    redis-cli hget node/1/vpn ip_address
    ${serial} =    Execute Command
    ...    runagent -m ${module_id} python3 -c "import os,sys; sys.path.insert(0, os.environ['AGENT_INSTALL_DIR'] + '/pypkg'); from pdnsmodule import dnsutil; print(dnsutil.soa_serial('${vpn}', '${ZONE}'))"
    RETURN    ${serial}

Open page
    [Arguments]    ${page}    ${heading}    ${shot}
    Go To    https://${NODE_ADDR}/cluster-admin/#/apps/${module_id}?page=${page}
    Wait For Elements State    iframe >>> h2 >> text="${heading}"    visible    timeout=30s
    Sleep    5s
    Take Screenshot    filename=${OUTPUT DIR}/browser/screenshot/${shot}.png

*** Test Cases ***
Check if powerdns is installed correctly
    ${output}  ${rc} =    Execute Command    add-module ${IMAGE_URL} 1
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{output} =    Evaluate    ${output}
    Set Global Variable    ${module_id}    ${output.module_id}

Take screenshots of the first configuration
    [Tags]    ui
    Import Library    Browser
    New Browser    chromium    headless=True
    New Context    ignoreHTTPSErrors=True
    Login to cluster-admin
    Open page    settings    Settings    1._First_configuration
    Close Browser

Check that an unconfigured instance has nothing to list
    ${config} =    Run action    get-configuration
    Should Not Be True    ${config}[configured]
    Refused action    list-zones    {}    not_configured

Check if powerdns can be configured as primary
    Run action    configure-module
    ...    {"role":"primary","ns_name":"ns1.robot.example","hostmaster":"hostmaster@robot.example","listen_addresses":[]}
    ${config} =    Run action    get-configuration
    Should Be Equal    ${config}[role]    primary
    Should Be True    ${config}[configured]

Check that the role cannot change
    Refused action    configure-module    {"role":"secondary","ns_name":"ns1.robot.example","primary":"x"}    role_change_not_supported

Check that the API key is not in the environment
    ${rc} =    Execute Command    runagent -m ${module_id} grep -qi api_key environment
    ...    return_rc=True  return_stdout=False
    Should Not Be Equal As Integers    ${rc}  0

Check that the service key is registered
    ${output} =    Execute Command    redis-cli hget module/${module_id}/srv/tcp/powerdns-api port
    Should Not Be Empty    ${output}

Check that a zone can be added and is served
    ${out} =    Run action    add-zone    {"zone":"${ZONE}"}
    Should Be Equal    ${out}[glue][0][ns_name]    ns1.robot.example
    ${serial} =    Serial on the VPN address
    Should Match Regexp    ${serial}    ^[0-9]+$

Check that records can be written
    Run action    set-records    {"zone":"${ZONE}","records":[{"name":"www","type":"A","ttl":300,"data":"192.0.2.1"},{"name":"@","type":"TXT","ttl":300,"data":"v=spf1 -all"}]}
    ${out} =    Run action    get-records    {"zone":"${ZONE}"}
    Should Be True    ${out}[editable]
    Refused action    set-records    {"zone":"${ZONE}","records":[{"name":"@","type":"NS","data":"x.example.org"}]}    apex_protected

Check that dnshelper can be given the provider configuration
    ${out} =    Run action    get-provider-config
    Should Be Equal    ${out}[provider]    powerdns
    Should Contain    ${out}[zones]    ${ZONE}

Check that DNSSEC can be enabled and shows a DS record
    ${out} =    Run action    update-zone    {"zone":"${ZONE}","dnssec":true}
    Should Be True    ${out}[dnssec]
    Should Match Regexp    ${out}[ds_records][0]    ^[0-9]+ 13 2 [0-9a-f]{64}$$

Take screenshots of the configured pages
    [Tags]    ui
    Import Library    Browser
    New Browser    chromium    headless=True
    New Context    ignoreHTTPSErrors=True
    Login to cluster-admin
    Open page    status    Status    2._Status
    Open page    settings    Settings    3._Settings
    Open page    zones    Zones    4._Zones
    Open page    records&zone=${ZONE}    Records    5._Records
    Open page    replication    Replication    6._Replication
    Open page    about    About    7._About
    Close Browser

Check that the backup scripts make a usable copy
    ${rc} =    Execute Command    runagent -m ${module_id} bash -c 'module-dump-state && test -s pdns.sqlite3.backup && module-cleanup-state'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0

Check that a zone can be removed
    Run action    remove-zone    {"zone":"${ZONE}"}
    ${serial} =    Serial on the VPN address
    Should Be Equal    ${serial}    None

Check if powerdns is removed correctly
    ${rc} =    Execute Command    remove-module --no-preserve ${module_id}
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
