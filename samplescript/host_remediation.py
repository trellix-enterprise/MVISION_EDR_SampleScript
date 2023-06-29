import json
import time
import controller
import urllib3
import configfile

class host_remediation(object):
    # Post a investigation request to retrieve the investigation id  -
    # using the payload "./payloads/HostBasedRemediation/postInvestigation.json"
    # evidenceType attribute in the payload "./payloads/HostBasedRemediation/postInvestigation.json" is set to "Device"
    # other Supported values are from the given list ["Device", "IP", "FQDN", "Identifier"]
    # the payload will map as below evidence type value: 
    # [IP: address, Device: hostName, FQDN: address, Identifier: id]
    def post_investigation(self):
        global Auth_token
        global headers
        Auth_token= "Bearer {}".format(controller.get_token(configfile.client_userid, configfile.client_credentials))
        headers = {
            'x-api-key': configfile.x_api_key,
            'Authorization': Auth_token,
            'Content-Type': 'application/vnd.api+json'
        }
        var_investigationid = " "
        with open('./payloads/HostBasedRemediation/postInvestigation.json') as json_path:
            investigation_payload = json_path.read()
        req_payload = json.loads(investigation_payload)
        req_payload["data"]["attributes"]["hostName"] = configfile.host_name
        investigation_url = "{}/edr/v2/investigations".format(configfile.base_url)
        
        print("\n***************Sending POST request for post_investigation********************")
        time.sleep(5)
        urllib3.disable_warnings()
        response = controller.callapirequest("Post-Investigation", "POST", investigation_url, headers, req_payload, False)
        response_status = response.status_code
        print("\nStatus code received for post_investigation: {}.\n\nResponse received for post_investigation:\n\n{}".format(response_status, response.text))
        
        if response_status == 201:
            var_investigationid = response.json()['data']['id']
        else:
            print("\nResponse error status code for post investigation is: {}. Stopping Execution.".format(response_status))
            controller.write_responsetoFile(response.text, './results/HostBasedRemediation/post_investigation_response.json')
            exit()
        controller.write_responsetoFile(response.text, './results/HostBasedRemediation/post_investigation_response.json')
        return var_investigationid

    # Request a GET call using the investigation id retrieved from previous post_investigation() function call
    # fetch all evidences for the investigation id of "Device" evidence type.
    # For Host based remediation we need to call the get-evidence api of "Device" evidence type
    # Returns the first Host name for the investigation id 
    def get_evidence(self,investigation_id):
        print("\n***************Sending GET request for get_evidence********************")
        var_host_name = " "
        investigation_url = "{}/edr/v2/investigations/investigation_id/evidence?evidenceType=Device".format(configfile.base_url)
        getevidence_url = investigation_url.replace("investigation_id", investigation_id)
        response = controller.callapirequest("Get-Evidence", "GET", getevidence_url, headers, False)
        response_status = response.status_code
        print("\nStatus code received for get_evidence: {}.\n\nResponse received for get_evidence:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            if response.json()['meta']['totalResourceCount'] != 0:
                var_host_name = response.json()['data']['attributes']['evidenceInfo'][0]['evidenceValue']["attributes"]["hostName"]
            else:
                print("\nNo records found to validate the get-evidence functionality!!!")
        else:
            print("\nResponse error Status code for get_evidence is: {}. Stopping Execution.".format(response_status))
            controller.write_responsetoFile(response.text, './results/HostBasedRemediation/get_evidence_response.json')
            exit()
        controller.write_responsetoFile(response.text, './results/HostBasedRemediation/get_evidence_response.json')
        return var_host_name

    # Request a POST call using the host name retrieved from previous get_evidence() function call
    # fetch all Agent GUIDS(hostids) for investigation.
    # Returns the Host guid for the host name    
    def get_metadata(self,host_name):
        print("\n***************Sending POST request for get_metadata********************")
        var_host_guid = " "
        with open('./payloads/HostBasedRemediation/getMetadata.json') as json_path:
            metadata_payload = json_path.read()
        req_payload = json.loads(metadata_payload)
        req_payload["data"]["attributes"]["hostNames"][0] = host_name
        metadata_url = "{}/edr/v2/investigations/metadata".format(configfile.base_url)
        response = controller.callapirequest("Get-Metadata", "POST", metadata_url, headers, req_payload, False)
        response_status = response.status_code
        print("\nStatus code received for get_metadata: {}.\n\nResponse received for get_metadata:\n\n{}".format(response_status, response.text))
        
        if response_status == 207: 
            if response.json()['meta']['totalResourceCount'] != 0:
                var_host_guid = response.json()['data']['attributes']['success'][0]['hostInfo'][0]['hostId']
            else:
                print("\nResponse returned error with failed status {}".format(response.json()['data']['attributes']['failed'][0]['status']))
                print("\nNo Host found for the used Tenant id to verify get-metadata functionality!!!")
                controller.write_responsetoFile(response.text, './results/HostBasedRemediation/get_metadata_response.json')
                exit()
        else:
            print("\nResponse error Status code for get_metadata is: {}. Stopping Execution.".format(response_status))
            controller.write_responsetoFile(response.text, './results/HostBasedRemediation/get_metadata_response.json')
            exit()
        controller.write_responsetoFile(response.text, './results/HostBasedRemediation/get_metadata_response.json')
        return var_host_guid

    # Request a POST call using the host guid and investigation id to take the action based on host connection status
    # creates a remediation action(Quarantine/Unuarantine) on the host 
    # Returns the remediation id starts with "hr-"
    def post_host_remediation(self, investigation_id, host_guid):
        print("\n***************Sending POST request for host_remediation********************")
        var_host_remid = " "
        with open('./payloads/HostBasedRemediation/hostbaseRemediation.json') as json_path:
            hostremediation_payload = json_path.read()
        req_payload = json.loads(hostremediation_payload)
        req_payload['data']['attributes']['investigationId'] = investigation_id
        req_payload['data']['attributes']['hostIds'][0] = host_guid
        hostremediation_url = "{}/edr/v2/remediation/host".format(configfile.base_url)
        print(req_payload)
        response = controller.callapirequest("Post-HostRemediation", "POST", hostremediation_url, headers, req_payload, False)
        response_status = response.status_code
        print("\nStatus code received for post_host_remediation:{}.\n\nResponse received for post_host_remediation:\n\n{}".format(response_status, response.text))
        
        if response_status == 207:
            if response.json()['data']['id'] != None: 
                var_host_remid = response.json()['data']['id']
            else:
                print("\nResponse returned error with failed status: {} \n\nand failed Message: {}  ".format(response.json()['data']['attributes']['failed'][0]['status'], response.json()['data']['attributes']['failed'][0]['message']))
                print("\nCalling Host Remediation API again by setting payload action attribute to QuarantineHost.")
                if(response.json()['data']['attributes']['failed'][0]['message'] == "Conflict, Host already in UnQuarantine state"):
                    req_payload['data']['attributes']['action'] = "QuarantineHost"   
                    response = controller.callapirequest("Post-HostRemediation", "POST", hostremediation_url, headers, req_payload, False)
                    response_status = response.status_code
                    print("\nStatus code received for post_host_remediation:{}.\n\nResponse received for post_host_remediation:\n\n{}".format(response_status, response.text))
                    if response_status == 207:
                        if response.json()['data']['id'] != None: 
                            var_host_remid = response.json()['data']['id']
                        else:
                            print("\nResponse returned error with failed status: {} \n\n and failed Message: {}  ".format(response.json()['data']['attributes']['failed'][0]['status'], response.json()['data']['attributes']['failed'][0]['message'])) 
                            controller.write_responsetoFile(response.text, './results/HostBasedRemediation/host_remediation_response.json')
                            exit()
        else:
            print("\nResponse error Status code for host_remediation is: {}. Stopping Execution.".format(response_status))
            controller.write_responsetoFile(response.text, './results/HostBasedRemediation/host_remediation_response.json')
            exit()
        controller.write_responsetoFile(response.text, './results/HostBasedRemediation/host_remediation_response.json')
        return var_host_remid
        
    # Request a GET call using the remediation id to get the status of the remediation action taken on the host
    # Returns the Host remediation status (in-progress/error-complete/completed etc)
    def get_hostremediation_status(self, host_remediationid):
        print("\n***************Sending GET request for host_remediation_status********************")
        var_host_rem_stats = " "
        investigation_url = "{}/edr/v2/remediation/queue-jobs/rem_id".format(configfile.base_url)
        hrstatus_url = investigation_url.replace("rem_id", host_remediationid)
        response = controller.callapirequest("Remediation_Status", "GET", hrstatus_url, headers, False)
        response_status = response.status_code
        print("\nStatus code received for get_hostremediation_status: {}.\nResponse received for get_hostremediation_status:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            var_host_rem_stats = response.json()['data']['attributes']['status']
            print("\nHost remediation status for remediation id {} : {}".format(host_remediationid, var_host_rem_stats))
        else:
            print("\nResponse error Status code for host_remediation_status is: {}.".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/HostBasedRemediation/host_remediationStatus_response.json')

def main(): 
    #removing response json files before execution starts
    controller.remove_filesfromdir("./results/HostBasedRemediation")   
    obj_hostrem =  host_remediation()
    print("\n*********************START OF HOST BASED REMEDIATION**************************")
    inv_id = obj_hostrem.post_investigation() # calling post Investigation API
    hostname = obj_hostrem.get_evidence(inv_id) # calling get evidence API
    hostguid = obj_hostrem.get_metadata(hostname) # calling post get metadata API
    hostremid = obj_hostrem.post_host_remediation(inv_id, hostguid) # calling post host remediation API
    obj_hostrem.get_hostremediation_status(hostremid) # calling get Host remediation status API
    print("\n*********************END OF HOST BASED REMEDIATION**************************")
    
if __name__=="__main__":
    main()
    