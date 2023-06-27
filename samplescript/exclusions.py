import json
import time
import controller
import urllib3
import configfile

class exclusions(object):
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
        var_hash_sha256 = 0
        getthreats_url = "{}/edr/v2/threats?page[offset]={}&page[limit]={}&from={}&sort={}".format(configfile.base_url, configfile.getthreats_offset, configfile.getthreats_pagelimit, configfile.getthreats_from, configfile.getthreats_sort)
        response = controller.callapirequest("Get-Threat", "GET", getthreats_url, headers, False)
        response_status = response.status_code
        print("\nStatus code received for get_threats: {}.\n\nResponse received for get_threats:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            if response.json()['meta']['totalResourceCount'] > 0:
                var_hash_sha256 =response.json()['data'][0]['attributes']['hashes']['sha256']
                print("\nGET request for Get-Threat api fetched {} records".format( response.json()['meta']['totalResourceCount']))
            else:
                print("\nNo threats found for the request.Exiting..")
                exit()
        else:
            print("\nResponse error Status code for get_threats is: {}. Stopping Execution.".format(response_status))
            controller.write_responsetoFile(response.text, './results/GetThreats/get_threats_response.json')
            exit()
        controller.write_responsetoFile(response.text, './results/GetThreats/get_threats_response.json')
        return var_hash_sha256
    
    #Post the exclusions api
    def post_exclusions(self, hash_sha256):
        with open('./payloads/Exclusions/post_exclusions.json') as json_path:
            exclusion_payload = json_path.read()
        req_payload = json.loads(exclusion_payload)
        req_payload["data"]["attributes"]["exclusionArguments"][0]["value"] = hash_sha256
        exclusions_url = "{}/edr/v2/remediation/exclusions".format(configfile.base_url)

        print("\n***************Sending POST request for post_exclusions********************")
        time.sleep(5)
        urllib3.disable_warnings()
        response = controller.callapirequest("Post-exclusions", "POST", exclusions_url, headers, req_payload, False)
        response_status = response.status_code
        print("\nStatus code received for post_exclusions: {}.\n\nResponse received for post_exclusions:\n\n{}".format(response_status, response.text))
        
        if response_status == 201:
            print("\nPost exclusions request sent Successfully")
        else:
            print("\nResponse error status code for post exclusions is: {}.".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/Exclusions/post_exclusions_response.json')
    
    # Get the exclusions api result
    # API response is written into  ./results/Exclusions/get_exclusions_response.json file
    def get_exclusions(self):       
        print("\n***************Sending GET request for exclusions********************")
        exclusionId = ""
        #To create the URL, make necessary changes in  configfile.py
        exclusion_url = "{}/edr/v2/remediation/exclusions".format(configfile.base_url)
        print("Exclusions URL is : {}".format(exclusion_url))
        # print("Exclusions header is : {}".format(headers))
        #call the get method for exclusion api
        response = controller.callapirequest("exclusion", "GET", exclusion_url, headers, False)        
        response_status = response.status_code
        print("\nStatus code received for exclusion API: {}.\n\nResponse received for get_exclusions:\n\n{}".format(response_status, response.text))
        if response_status == 200:
            if response.json()['meta']['totalResourceCount'] > 0:
                exclusionId = response.json()['data'][0]['id']
                print("\nGET request for exclusions fetched {} records".format( response.json()['meta']['totalResourceCount']))
            else:
                print("\nNo records found to validate the exclusion functionality!!!")
        else:
            print("\nResponse error Status code for get_exclusions is: {}".format(response_status))
            
        # Write the response Json to /results/ActionHistory/get_actionhistory_response.json file
        controller.write_responsetoFile(response.text, './results/Exclusions/get_exclusions_response.json')
        return exclusionId
    
    # Retrieve exclusions by exclusion ID
    def get_exclusionsByExclusionId(self, exclusion_id):
        print("\n***************Sending GET request for get_exclusion_by_exclusionId********************")
        getexclusionbyexclusionid = "{}/edr/v2/remediation/exclusions/{}".format(configfile.base_url, exclusion_id)
        response = controller.callapirequest("Get-ExclusionbyExclusionId", "GET", getexclusionbyexclusionid, headers, False)        
        response_status = response.status_code
        print("\nStatus code received for get_exclusion_by_exclusionId: {}.\n\nResponse received for get_exclusion_by_exclusionId:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            if response.json()['meta']['totalResourceCount'] > 0:
                print("\nGET request for get-exclusions By Exclusion ID is Successful")
            else:
                print("\nNo records found to validate the exclusion functionality!!!")
        else:
            print("\nResponse error Status code for get_exclusions is: {}".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/Exclusions/get_exclusions_by_exclusion_id_response.json')

    #Patch the exclusions api
    def patch_exclusions(self, exclusion_id, hash_sha256):
        with open('./payloads/Exclusions/patch_exclusions.json') as json_path:
            exclusion_payload = json_path.read()
        req_payload = json.loads(exclusion_payload)
        req_payload["data"]["id"] = exclusion_id
        # req_payload["data"]["attributes"]["exclusionArguments"][0]["value"] = "1234"
        exclusions_url = "{}/edr/v2/remediation/exclusions/{}".format(configfile.base_url, exclusion_id)

        print("\n***************Sending PATCH request for patch_exclusions********************")
        time.sleep(5)
        urllib3.disable_warnings()
        response = controller.callapirequest("Patch-exclusions", "PATCH", exclusions_url, headers, req_payload, False)
        response_status = response.status_code
        print("\nStatus code received for patch_exclusions: {}.\n\nResponse received for patch_exclusions:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            print("\nPatch exclusions request sent Successfully")
        else:
            print("\nResponse error status code for patch exclusions is: {}.".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/Exclusions/patch_exclusions_response.json')
        
    # Delete exclusions by exclusion ID
    def delete_exclusionsByExclusionId(self, exclusion_id):
        print("\n***************Sending DELETE request for delete_exclusion_by_exclusionId********************")
        deleteexclusionbyexclusionid = "{}/edr/v2/remediation/exclusions/{}".format(configfile.base_url, exclusion_id)
        response = controller.callapirequest("Delete-ExclusionbyExclusionId", "DELETE", deleteexclusionbyexclusionid, headers, False)        
        response_status = response.status_code
        print("\nStatus code received for delete_exclusion_by_exclusionId: {}.\n\nResponse received for delete_exclusion_by_exclusionId:\n\n{}".format(response_status, response.text))
        
        if response_status == 204:
            print("\nDELETE request for delete-exclusions By Exclusion ID is Successful")
        else:
            print("\nResponse error Status code for delete_exclusions is: {}".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/Exclusions/delete_exclusions_by_exclusion_id_response.json')
      
def main():   
    #removing response json files before execution starts
    controller.remove_filesfromdir("./results/Exclusions") 
    obj_exclusions = exclusions()
    print("\n*********************START OF EXCLUSIONS***********************")
    hash_sha256 = obj_exclusions.get_threats() # calling Get-threats API
    obj_exclusions.post_exclusions(hash_sha256) # calling Post exclusion API
    exclusion_id = obj_exclusions.get_exclusions()   # calling get exclusion API
    obj_exclusions.patch_exclusions(exclusion_id, hash_sha256) # calling Patch exclusion API
    obj_exclusions.get_exclusionsByExclusionId(exclusion_id)   # calling get exclusion by exclusion ID API
    obj_exclusions.delete_exclusionsByExclusionId(exclusion_id) # calling delete exclusion by exclusion ID API
    print("\n*********************END OF EXCLUSIONS**************************")

#Main Function    
if __name__=="__main__":
    main()