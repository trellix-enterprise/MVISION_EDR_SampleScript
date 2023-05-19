import logging
import json
import requests
import time
from requests.models import Response
import controller
import urllib3
import configfile

class get_remediation(object):
    # Get Threats info on basis of time. 
    # By default last 7 days data is pulled when "from" is not mentioned in the query param.
    # Default page[limit] is 20 and max page[limit] is 20,000
    # Returns first threat id
    def get_threats(self):
        global Auth_token
        global headers
        Auth_token= "Bearer {}".format(controller.get_token(configfile.gtclient_id, configfile.gtclient_credentials))
        headers = {
            'x-api-key': configfile.x_api_key,
            'Authorization': Auth_token,
            'Content-Type': 'application/vnd.api+json'
        }        
        print("\n***************Sending GET request for get_threats********************")
        var_threat_id = ""
        getthreats_url = "{}/edr/v2/threats?page[offset]={}&page[limit]={}&from={}&sort={}".format(configfile.base_url, configfile.getthreats_offset, configfile.getthreats_pagelimit, configfile.getthreats_from, configfile.getthreats_sort)
        response = controller.callapirequest("Get-Threat", "GET", getthreats_url, headers, False)
        response_status = response.status_code
        print("\nStatus code received for get_threats: {}.\n\nResponse received for get_threats:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            if response.json()['meta']['totalResourceCount'] > 0:
                var_threat_id =response.json()['data'][0]['id']
                print("\nGET request for Get-Threat api fetched {} records".format( response.json()['meta']['totalResourceCount']))
            else:
                print("\nNo threats found for the request.Exiting..")
                exit()
        else:
            print("\nResponse error Status code for get_threats is: {}. Stopping Execution.".format(response_status))
            controller.write_responsetoFile(response.text, './results/GetThreats/get_threats_response.json')
            exit()
        controller.write_responsetoFile(response.text, './results/GetThreats/get_threats_response.json')
        return var_threat_id

    # Retrieve threat's affected hosts
    def get_threatsbyaffectedhost(self, threat_id):
        print("\n***************Sending GET request for get_threats_affectedHost********************")
        affected_host_id = ""
        getthreatsbyhost_url = "{}/edr/v2/threats/{}/affectedhosts?page[offset]={}&page[limit]={}&from={}&sort={}".format(configfile.base_url, threat_id, configfile.getthreats_offset, configfile.getthreats_pagelimit, configfile.getthreats_from, configfile.getthreats_sort)
        response = controller.callapirequest("Get-ThreatbyAffectedHost", "GET", getthreatsbyhost_url, headers, False)        
        response_status = response.status_code
        print("\nStatus code received for get_threats_affectedHost: {}.\n\nResponse received for get_threats_affectedHost:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            if response.json()['meta']['totalResourceCount'] > 0:
                affected_host_id = response.json()['data'][0]['id']
                print("\nGET request for Get-Threat api fetched {} records".format( response.json()['meta']['totalResourceCount']))
                print("\nGET request for get-threats affected Host is Successful")
            else:
                print("\nNo threats found for the Affected host threat id.")
        else:
            print("\nResponse error Status code for get_threatsaffectedHost is: {}. Stopping Execution.".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/GetThreats/get_threatsaffectedHost_response.json')
        return affected_host_id
    
    # Post a remediation request to retrieve the remediation id  -
    # using the payload "./payloads/ThreatBasedRemediation/postremediation.json"
    def post_remediation(self, threat_id, res_host):
        with open('./payloads/ThreatBasedRemediation/threatbasedRemediation.json') as json_path:
            remediation_payload = json_path.read()
        req_payload = json.loads(remediation_payload)
        req_payload["data"]["attributes"]["threatId"] = threat_id
        req_payload["data"]["attributes"]["affectedHostIds"][0] = res_host
        remediation_url = "{}/edr/v2/remediation/threat".format(configfile.base_url)

        print("\n***************Sending POST request for post_remediation********************")
        time.sleep(5)
        urllib3.disable_warnings()
        response = controller.callapirequest("Post-remediation", "POST", remediation_url, headers, req_payload, False)
        response_status = response.status_code
        print("\nStatus code received for post_remediation: {}.\n\nResponse received for post_remediation:\n\n{}".format(response_status, response.text))
        
        if response_status == 207:
            print("\nPost remediation request sent Successfully")
        else:
            print("\nResponse error status code for post remediation is: {}.".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/ThreatBasedRemediation/post_remediation_response.json')
    
    def post_global_threat_remediation(self, threat_id):        
        with open('./payloads/ThreatBasedRemediation/globalthreatbasedRemediation.json') as json_path:
            remediation_payload = json_path.read()
        req_payload = json.loads(remediation_payload)
        req_payload["data"]["attributes"]["threatActionArguments"]["threatId"] = threat_id
        remediation_url = "{}/edr/v2/remediation/global-threat".format(configfile.base_url)
        
        print("\n***************Sending POST request for post_global_threat_remediation********************")
        time.sleep(5)
        urllib3.disable_warnings()
        response = controller.callapirequest("Post-global-threat-remediation", "POST", remediation_url, headers, req_payload, False)
        response_status = response.status_code
        print("\nStatus code received for post_global_threat_remediation: {}.\n\nResponse received for post_global_threat_remediation:\n\n{}".format(response_status, response.text))
        
        if response_status == 201:
            print("\nPost remediation request sent Successfully")
        else:
            print("\nResponse error status code for post global threat remediation is: {}.".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/ThreatBasedRemediation/post_global_threat_remediation_response.json')
                
def main(): 
    #removing response json files before execution starts
    controller.remove_filesfromdir("./results/ThreatBasedRemediation")   
    controller.remove_filesfromdir("./results/GetThreats")   
    obj_getremediation =  get_remediation()
    print("\n*********************START OF THREAT BASED REMEDIATION**************************")
    threat_id = obj_getremediation.get_threats() # calling Get-threats API
    res_host = obj_getremediation.get_threatsbyaffectedhost(threat_id) #calling Get-threats by infected host API
    obj_getremediation.post_remediation(threat_id, res_host) # calling post Remediation API
    obj_getremediation.post_global_threat_remediation(threat_id) # calling post global threat based Remediation API
    print("\n*********************END OF POST REMEDIATION**************************")
    
if __name__=="__main__":
    main()