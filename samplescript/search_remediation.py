import logging
import json ,ast
import csv
import requests
import time
from requests.models import Response
import controller
import urllib3
import configfile

class search_remediation(object):
    # Request a POST call to create a RTS search
    # Returns the RTS search id to fetch the RTS search status and search result
    def post_ARcreatesearch(self):
        global Auth_token
        global headers
        Auth_token= "Bearer {}".format(controller.get_token(configfile.client_userid, configfile.client_credentials))
        headers = {
            'x-api-key': configfile.x_api_key,
            'Authorization': Auth_token,
            'Content-Type': 'application/vnd.api+json'
        }
        var_RTSsearchid = " "
        with open('./payloads/SearchBasedRemediation/createARsearch.json') as json_path:
            rtssearch_payload = json_path.read()
        req_payload = json.loads(rtssearch_payload)
        req_payload["data"]["attributes"]["query"] = configfile.rts_query_name
        rtssearch_url = "{}/edr/v2/searches/realtime".format(configfile.base_url)
        
        print("\n***************Sending POST request for RTS create_search********************")
        time.sleep(5)
        urllib3.disable_warnings()
        response = controller.callapirequest("Post-ARSearch", "POST", rtssearch_url, headers, req_payload, False)
        response_status = response.status_code
        print("\nStatus code received for post_ARcreatesearch:{}.\n\nResponse received for post_ARcreatesearch:\n\n{}".format(response_status, response.text))
        
        if response_status == 201:
            var_RTSsearchid = response.json()['data']['id']
        else:
            print("\nResponse error status code for RTS create search is: {}. Stopping Execution.".format(response_status))
            controller.write_responsetoFile(response.text, './results/SearchBasedRemediation/rts_createsearch_response.json')
            exit()
        controller.write_responsetoFile(response.text, './results/SearchBasedRemediation/rts_createsearch_response.json')
        return var_RTSsearchid

    # Request a GET call to fetch the RTS search status using the search id 
    def get_RTSsearchstatus(self,search_id):
        print("\n***************Sending GET request for RTS get_status********************")
        status_url = "{}/edr/v2/searches/queue-jobs/{}".format(configfile.base_url,search_id)
        response = requests.request("GET", status_url, headers=headers, allow_redirects=False)
        response_status = response.status_code
        print("\nStatus code received for get_RTSsearchstatus: {}.\n\nResponse received for get_RTSsearchstatus:\n\n{}".format(response_status, response.text))
        
        time.sleep(15)
        if response_status == 200:
            status = True
            retry = 0
            max_attempt = 10
            while status:
                if retry < max_attempt:
                    retry_response = requests.request("GET", status_url, headers=headers, allow_redirects=False)
                    if retry_response.status_code != 303 and retry_response.status_code == 200:
                        print("\n{}. Status is inprogress, sleep for 15 seconds".format(retry+1))
                        time.sleep(15)
                        retry += 1
                        continue
                    print("\nStatus code for RTS get status is {}".format(retry_response.status_code))
                status = False
                break
        else:
            print("\nResponse error status code for RTS get status is: {}. Stopping Execution.".format(response_status.status_code))
            exit()

    # Request a GET call to fetch the RTS search results using the search id 
    # Returns the first row id from search result 
    def get_RTSsearchresult(self, search_id):
        var_RTSrowid = " "
        print("\n***************Sending GET request for RTS get_result********************")
        status_url = "{}/edr/v2/searches/realtime/{}/results".format(configfile.base_url,search_id)
        response = requests.request("GET", status_url, headers=headers)
        response_status = response.status_code
        print("\nStatus code received for get_RTSsearchresult: {}.\n\nResponse received for get_RTSsearchresult\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            var_RTSrowid = response.json()['data'][0]['id']
        else:
            print("\nResponse error status code for RTS get status is: {}. Stopping Execution.".format(retry_response.status_code))
            controller.write_responsetoFile(response.text, './results/SearchBasedRemediation/rts_getresult_response.json')
            exit()
        controller.write_responsetoFile(response.text, './results/SearchBasedRemediation/rts_getresult_response.json')
        return var_RTSrowid
        
    # Request a POST call using the RTS raw id and search id id to take the action mentioned in payload
    # creates a remediation action on the host based on search result
    # Returns the remediation id starts with "sr-"
    def post_searchremediation(self,action_name, search_id, row_id):
        if action_name == "QuarantineHost" or action_name == "UnquarantineHost":
            with open('./payloads/SearchBasedRemediation/searchbaseRemediation.json') as json_path:
                searchremediation_payload = json_path.read()
        else:
            with open('./payloads/SearchBasedRemediation/SearchBasedRemediation_nonHost.json') as json_path:
                searchremediation_payload = json_path.read()
        req_payload = json.loads(searchremediation_payload)
        req_payload["data"]["attributes"]["action"] = action_name
        req_payload["data"]["attributes"]["searchId"] = search_id
        req_payload["data"]["attributes"]["rowIds"][0] = row_id
        req_payload["data"]["attributes"]["actionInputs"][0]["name"] = configfile.searchrem_action_input_name
        req_payload["data"]["attributes"]["actionInputs"][0]["value"] = configfile.searchrem_action_input_value
        searchremediation_url = "{}/edr/v2/remediation/search".format(configfile.base_url)
        var_search_remid = " "
        print("\n***************Sending POST request for RTS post_searchremediation********************")
        time.sleep(5)
        urllib3.disable_warnings()
        response = controller.callapirequest("Post-SearchRemediation", "POST", searchremediation_url, headers, req_payload, False)
        response_status = response.status_code
        print("\nStatus code received for post_searchremediation: {}.\n\nResponse received for post_searchremediation:\n\n{}".format(response_status, response.text))
        
        if response_status == 207:
            if response.json()['data']['id'] != None: 
                var_search_remid = response.json()['data']['id']
                print("\nsearch remediation id created : {}".format(var_search_remid))
            else:
                print("\nResponse returned error with failed status: {} \n\n and failed Message: {}  ".format(response.json()['data']['attributes']['failed'][0]['status'], response.json()['data']['attributes']['failed'][0]['message'])) 
                controller.write_responsetoFile(response.text, './results/SearchBasedRemediation/searchremediation_response.json')
                exit()
        else:
            print("\nResponse error status code for RTS create search is: {}. Stopping Execution.".format(response_status))
            controller.write_responsetoFile(response.text, './results/SearchBasedRemediation/searchremediation_response.json')
            exit()
        controller.write_responsetoFile(response.text, './results/SearchBasedRemediation/searchremediation_response.json')
        return var_search_remid

    # Request a GET call using the remediation id to get the status of the remediation action taken on the host
    # Returns the search remediation status (in-progress/error-complete/completed etc)
    def get_searchremediation_status(self, search_remediationid):
        print("\n***************Sending GET request for host_remediation_status********************")
        var_search_rem_stats = " "
        investigation_url = "{}/edr/v2/remediation/queue-jobs/rem_id".format(configfile.base_url)
        srstatus_url = investigation_url.replace("rem_id", search_remediationid)
        response = controller.callapirequest("SearchRemediation_Status", "GET", srstatus_url, headers, False)
        response_status = response.status_code
        print("\nStatus code received for get_searchremediation_status: {}.\n\nResponse received for get_searchremediation_status:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            var_search_rem_stats = response.json()['data']['attributes']['status']
            print("\nSearch remediation status for remediation id {} : {}".format(search_remediationid, var_search_rem_stats))
        else:
            print("\nResponse error Status code for host_remediation_status is: {}. Stopping Execution.".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/SearchBasedRemediation/search_remediationStatus_response.json')  
        
def main(): 
    #removing response json files before execution starts
    controller.remove_filesfromdir("./results/SearchBasedRemediation")       
    obj_srchrem =  search_remediation()
    print("\n*********************START OF SEARCHED BASED REMEDIATION**************************")
    rtssearch_id = obj_srchrem.post_ARcreatesearch() # calling post create RTS search API
    obj_srchrem.get_RTSsearchstatus(rtssearch_id) # calling get status RTS search API
    rtsrow_id = obj_srchrem.get_RTSsearchresult(rtssearch_id) # calling get result RTS search API
    action_name = configfile.searchrem_action_name
    print("\nSearch remediation action set to: {}".format(action_name))
    searchremid = obj_srchrem.post_searchremediation(action_name, rtssearch_id, rtsrow_id) # calling post Search remediation API
    obj_srchrem.get_searchremediation_status(searchremid) # calling get Search remediation status API
    print("\n*********************END OF SEARCHED BASED REMEDIATION**************************")

if __name__=="__main__":
    main()