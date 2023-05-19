import logging
import json
import requests
import time
from requests.models import Response
import controller
import urllib3
import configfile

class get_metadata(object):
    # Post a investigation request to retrieve the investigation id  -
    # using the payload "./payloads/HostBasedRemediation/postInvestigation.json"
    # evidenceType attribute in the payload "./payloads/HostBasedRemediation/postInvestigation.json" is set to "Device"
    # other Supported values are from the given list ["Device", "IP", "FQDN", "Identifier"]
    # the payload will map as below evidence type value: 
    # [IP: address, Device: hostName, FQDN: address, Identifier: id]
    def post_investigation(self):
        global Auth_token
        global headers
        #Generate Authentication Token, change the tenant_username and tenant_password in configfile.py
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
            controller.write_responsetoFile(response.text, './results/GetMetadata/post_investigation_response.json')
            exit()
        controller.write_responsetoFile(response.text, './results/GetMetadata/post_investigation_response.json')
        return var_investigationid

    # Request a GET call using the investigation id retrieved from previous post_investigation() function call
    # fetch all evidences for the investigation id.
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
                print("\nNo records found for the used Tenant id, Please use a different tenant to test the get-evidence functionality!!!")
        else:
            print("\nResponse error Status code for get_evidence is: {}. Stopping Execution.".format(response_status))
            controller.write_responsetoFile(response.text, './results/GetMetadata/get_evidence_response.json')
            exit()
        controller.write_responsetoFile(response.text, './results/GetMetadata/get_evidence_response.json')
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
        response = requests.post(metadata_url, headers=headers, data=json.dumps(req_payload), verify=False)
        response_status = response.status_code
        print("\nStatus code received for get_metadata: {}.\n\nResponse received for get_metadata:\n\n{}".format(response_status, response.text))
        
        if response_status == 207:
            if response.json()['meta']['totalResourceCount'] != 0:
                print("\nGET request for Get Metadata fetched {} records".format( response.json()['meta']['totalResourceCount']))
            else:
                print("\nNo Host records found to validate the get-metadata functionality!!!")
                print("\nResponse returned error with failed status {}".format(response.json()['data']['attributes']['failed'][0]['status']))
        else:
            print("\nResponse error Status code for get_metadata is: {}.".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/GetMetadata/get_metadata_response.json')
        
def main():  
    #removing response json files before execution starts
    controller.remove_filesfromdir("./results/GetMetadata") 
    obj_getmetadata =  get_metadata()
    print("\n*********************START OF GET METADATA**********************")
    inv_id = obj_getmetadata.post_investigation() # calling post Investigation API
    hostname = obj_getmetadata.get_evidence(inv_id) # calling get evidence API
    obj_getmetadata.get_metadata(hostname) # calling post get metadata API
    print("\n*********************END OF GET METADATA**************************")

#Main Function
if __name__=="__main__":
    main()