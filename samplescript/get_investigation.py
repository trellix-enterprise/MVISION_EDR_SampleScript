import json
import time
import controller
import urllib3
import configfile

class get_investigation(object):
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
            print("\nPost Investigation request sent Successfully")
        else:
            print("\nResponse error status code for post investigation is: {}.".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/GetInvestigation/post_investigation_response.json')
        
    # Get call to fetch all investigation request 
    def get_investigation(self):
        print("\n***************Sending GET request for get_investigation********************")
        var_host_name = " "
        getinvestigation_url = "{}/edr/v2/investigations".format(configfile.base_url)
        response = controller.callapirequest("Get-Investigation", "GET", getinvestigation_url, headers, False)
        response_status = response.status_code
        print("\nStatus code received for get_investigation:{}.\n\nResponse received for get_investigation:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            if response.json()['meta']['totalResourceCount'] != 0:
                print("\nGET request for Get Investigations fetched {} records".format( response.json()['meta']['totalResourceCount']))
            else:
                print("\nNo records found to validate the get-investigation functionality!!!")
        else:
            print("\nResponse error Status code for get_investigation is: {}.".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/GetInvestigation/get_investigation_response.json')
    
    # Get call to fetch all investigation request with "include" parameter; Available values : "evidence"
    # include param is used to get extra information with response like evidence with investigation response will come with relationship
    def get_investigationwithincludeparam(self):
        print("\n***************Sending GET request for get_investigationwithincludeparam********************")
        var_host_name = " "
        getinvestigation_url = "{}/edr/v2/investigations?include=evidence".format(configfile.base_url)
        response = controller.callapirequest("Get-InvestigationwithIncludeparam", "GET", getinvestigation_url, headers, False)
        response_status = response.status_code
        print("\nStatus code received for get_investigationwithincludeparam: {}.\n\nResponse received for get_investigationwithincludeparam:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            if response.json()['meta']['totalResourceCount'] != 0:
                print("\nGET request for Get Investigations with include param fetched {} records".format( response.json()['meta']['totalResourceCount']))
            else:
                print("\nNo records found to validate the get-investigationwithincludeparam functionality!!!")
        else:
            print("\nResponse error Status code for get_investigationwithincludeparam is: {}.".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/GetInvestigation/get_investigation_withincludeparam_response.json')
                
def main(): 
    #removing response json files before execution starts
    controller.remove_filesfromdir("./results/GetInvestigation")   
    obj_getinvestigation =  get_investigation()
    print("\n*********************START OF GET INVESTIGATION**************************")
    obj_getinvestigation.post_investigation() # calling post Investigation API
    obj_getinvestigation.get_investigation() # calling get investigation API
    obj_getinvestigation.get_investigationwithincludeparam() # calling get investigation API with include param
    print("\n*********************END OF GET INVESTIGATION**************************")
    
if __name__=="__main__":
    main()