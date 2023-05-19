import logging
import json
import requests
import time
from requests.models import Response
import controller
import urllib3
import configfile

class get_evidence(object):
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
            controller.write_responsetoFile(response.text, './results/GetEvidence/post_investigation_response.json')
            exit()
        controller.write_responsetoFile(response.text, './results/GetEvidence/post_investigation_response.json')
        return var_investigationid
        
    # Request a GET call using the investigation id retrieved from previous post_investigation() function call
    # fetch all evidences for the investigation id.
    # Returns the first Host name for the investigation id
    # calling get evidence API with investigation id and the Evidence_type
    # The Evidence_type value supported is from below list. It could be one or multiple values with comma separated 
    # "Device" or "Device,IP,FQDN"
    #Evidence_type = ["Device", "IP", "FQDN", "Identifier"]
    def get_evidence(self,investigation_id, evidence_type = None):
        print("\n***************Sending GET request for get_evidence with Evidence type {}********************".format(evidence_type))
        var_host_name = " "
        if evidence_type != None:
            investigation_url = "{}/edr/v2/investigations/investigation_id/evidence?evidenceType={}".format(configfile.base_url, evidence_type)
        else:
            investigation_url = "{}/edr/v2/investigations/investigation_id/evidence".format(configfile.base_url)
        print (investigation_url)
        getevidence_url = investigation_url.replace("investigation_id", investigation_id)
        response = controller.callapirequest("Get-Evidence", "GET", getevidence_url, headers, False)
        response_status = response.status_code
        print("\nStatus code received for get_evidence: {}.\n\nResponse received for get_evidence:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            if response.json()['meta']['totalResourceCount'] != 0:
                print("\nGET request for Get Evidence fetched {} records".format( response.json()['meta']['totalResourceCount']))
            else:
                print("\nNo records found to validate the get-evidence functionality!!!")
        else:
            print("\nResponse error Status code for get_evidence is: {}.".format(response_status))
        if evidence_type == None:    
            controller.write_responsetoFile(response.text, './results/GetEvidence/get_evidence_response.json')
        else:
             controller.write_responsetoFile(response.text, './results/GetEvidence/get_evidence_with_evidencetype_response.json')

def main(): 
    #removing response json files before execution starts
    controller.remove_filesfromdir("./results/GetEvidence")   
    obj_getevidence =  get_evidence()
    print("\n*********************START OF GET EVIDENCE**************************")
    inv_id = obj_getevidence.post_investigation() # calling post Investigation API
    obj_getevidence.get_evidence(inv_id) # calling get evidence API with only investigation id to get all the evidences
    obj_getevidence.get_evidence(inv_id, "Device") # calling get evidence API with investigation id and the Evidence_type
                                                   # The Evidence_type value supported is from below list. 
                                                   #Evidence_type = ["Device", "IP", "FQDN", "Identifier"]
    print("\n*********************END OF GET EVIDENCE**************************")
    
if __name__=="__main__":
    main()