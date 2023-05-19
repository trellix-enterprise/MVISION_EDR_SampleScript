import logging
import json
import requests
import time
from requests.models import Response
import controller
import urllib3
import configfile

class threats(object):
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

    # Get Threats info on basis of given threatId
    def get_threatsbyid(self, threat_id):
        print("\n***************Sending GET request for get_threats_withID********************")
        getthreatsbyid_url = "{}/edr/v2/threats/{}".format(configfile.base_url, threat_id)
        response = controller.callapirequest("Get-ThreatbyID", "GET", getthreatsbyid_url, headers, False)      
        response_status = response.status_code
        print("\nStatus code received for get_threats_withID: {}.\n\nResponse received for get_threats_withID:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            if response.json()['meta']['totalResourceCount'] > 0:
                print("\nGET request for Get-Threat api fetched {} records".format( response.json()['meta']['totalResourceCount']))
                print("\nGET request for get-threats with ID is Successful")
            else:
                print("\nNo threats found for the threat id.")
        else:
            print("\nResponse error Status code for get_threatswithID is: {}. Stopping Execution.".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/GetThreats/get_threatswithID_response.json')

    # Retrieve threat's affected hosts
    def get_threatsbyaffectedhost(self, threat_id):
        print("\n***************Sending GET request for get_threats_affectedHost********************")
        getthreatsbyhost_url = "{}/edr/v2/threats/{}/affectedhosts?page[offset]={}&page[limit]={}&from={}&sort={}".format(configfile.base_url, threat_id, configfile.getthreats_offset, configfile.getthreats_pagelimit, configfile.getthreats_from, configfile.getthreats_sort)
        response = controller.callapirequest("Get-ThreatbyAffectedHost", "GET", getthreatsbyhost_url, headers, False)        
        response_status = response.status_code
        print("\nStatus code received for get_threats_affectedHost: {}.\n\nResponse received for get_threats_affectedHost:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            if response.json()['meta']['totalResourceCount'] > 0:
                print("\nGET request for Get-Threat api fetched {} records".format( response.json()['meta']['totalResourceCount']))
                print("\nGET request for get-threats affected Host is Successful")
            else:
                print("\nNo threats found for the Affected host threat id.")
        else:
            print("\nResponse error Status code for get_threatsaffectedHost is: {}. Stopping Execution.".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/GetThreats/get_threatsaffectedHost_response.json')

    # Retrieve threat's detection data
    def get_threatsdetection(self, threat_id):
        print("\n***************Sending GET request for get_threatsdetection********************")
        getthreatsdetection_url = "{}/edr/v2/threats/{}/detections?page[offset]={}&page[limit]={}&from={}&sort={}".format(configfile.base_url, threat_id, configfile.getthreats_offset, configfile.getthreats_pagelimit, configfile.getthreats_from, configfile.getthreats_sort)
        response = controller.callapirequest("Get-ThreatbyDetection", "GET", getthreatsdetection_url, headers, False)       
        response_status = response.status_code
        print("\nStatus code received for get_threats_detection: {}.\n\nResponse received for get_threats_detection:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            if response.json()['meta']['totalResourceCount'] > 0:
                print("\nGET request for Get-Threat api fetched {} records".format( response.json()['meta']['totalResourceCount']))
                print("\nGET request for get-threats detection is Successful")
            else:
                print("\nNo threats found for the threat detection threat id.")
        else:
            print("\nResponse error Status code for get_threatsdetection is: {}. Stopping Execution.".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/GetThreats/get_threatsdetections_response.json')

    # Get Threats info with include parameter
    # include param is used to get extra information with response like detection,affecteshost 
    # with threats response will come with relationship
    # Available values : affectedhosts, detections
    def get_threatswithincludeparam(self):
        print("\n***************Sending GET request for get_threatswithincludeparam********************")
        getthreatsincludeparam_url = "{}/edr/v2/threats?include=affectedhosts,detections&page[offset]={}&page[limit]={}&from={}&sort={}".format(configfile.base_url, configfile.getthreats_offset, configfile.getthreats_pagelimit, configfile.getthreats_from, configfile.getthreats_sort)
        response = controller.callapirequest("Get-ThreatwithIncludeParam", "GET", getthreatsincludeparam_url, headers, False)       
        response_status = response.status_code
        print("\nStatus code received for get_threats_includeparam: {}.\n\nResponse received for get_threats_includeparam:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            if response.json()['meta']['totalResourceCount'] > 0:
                print("\nGET request for Get-Threat api fetched {} records".format( response.json()['meta']['totalResourceCount']))
                print("\nGET request for-get threats with include parameter is Successful")
            else:
                print("\nNo threats found for the threat detection threat id.")
        else:
            print("\nResponse error Status code for get_threatswithincludeparam is: {}. Stopping Execution.".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/GetThreats/get_threatswithincludeparam_response.json')

def main():   
    #removing response json files before execution starts
    controller.remove_filesfromdir("./results/GetThreats") 
    obj_getthreats =  threats()
    print("\n*********************START OF GET THREATS***********************")
    threat_id = obj_getthreats.get_threats() # calling Get-threats API
    res_id = obj_getthreats.get_threatsbyid(threat_id) # calling Get-threats by ID API 
    res_host = obj_getthreats.get_threatsbyaffectedhost(threat_id) #calling Get-threats by infected host API
    res_detection = obj_getthreats.get_threatsdetection(threat_id) #calling Get-threats detection API
    obj_getthreats.get_threatswithincludeparam() #calling Get-threats with include param API
    print("\n*********************END OF GET THREATS**************************")
    
if __name__=="__main__":
    main()