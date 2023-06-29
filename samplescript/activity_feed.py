import logging
import json
import requests
import time
from requests.models import Response
import controller
import urllib3
import configfile

class activity_feed(object):    
    #Post the activity feed api
    def post_activity_feed(self):
        global Auth_token
        global headers
        Auth_token= "Bearer {}".format(controller.get_token(configfile.client_userid, configfile.client_credentials))
        headers = {
            'x-api-key': configfile.x_api_key,
            'Authorization': Auth_token,
            'Content-Type': 'application/vnd.api+json'
        }
        with open('./payloads/ActivityFeed/post_activity_feed.json') as json_path:
            activity_feed_payload = json_path.read()
        req_payload = json.loads(activity_feed_payload)
        activity_feed_url = "{}/edr/v2/activity-feed/configurations".format(configfile.base_url)

        print("\n***************Sending POST request for post Activity Feed********************")
        time.sleep(5)
        urllib3.disable_warnings()
        response = controller.callapirequest("Post-activity_feed", "POST", activity_feed_url, headers, req_payload, False)
        response_status = response.status_code
        print("\nStatus code received for post activity_feed: {}.\n\nResponse received for post activity_feed:\n\n{}".format(response_status, response.text))
        
        if response_status == 201:
            print("\nPost activity_feed request sent Successfully")
        else:
            print("\nResponse error status code for post activity_feed is: {}.".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/ActivityFeed/post_activity_feed_response.json')
    
    # Get the activity_feed api result
    # API response is written into  ./results/activity_feed/get_activity_feed_response.json file
    def get_activity_feed(self):       
        print("\n***************Sending GET request for Activity Feed********************")
        activityFeedId = ""
        #To create the URL, make necessary changes in  configfile.py
        activity_feed_url = "{}/edr/v2/activity-feed/configurations".format(configfile.base_url)
        print("activity_feed URL is : {}".format(activity_feed_url))
        # print("activity_feed header is : {}".format(headers))
        #call the get method for activity_feed api
        response = controller.callapirequest("activity_feed", "GET", activity_feed_url, headers, False)        
        response_status = response.status_code
        print("\nStatus code received for Activity Feed API: {}.\n\nResponse received for get_activity_feed:\n\n{}".format(response_status, response.text))
        if response_status == 200:
            if response.json()['meta']['totalResourceCount'] > 0:
                activityFeedId = response.json()['data'][0]['id']
                print("\nGET request for activity_feed fetched {} records".format( response.json()['meta']['totalResourceCount']))
            else:
                print("\nNo records found to validate the activity_feed functionality!!!")
        else:
            print("\nResponse error Status code for get_activity_feed is: {}".format(response_status))
            
        # Write the response Json to /results/ActivityFeed/get_activity_feed_response.json file
        controller.write_responsetoFile(response.text, './results/ActivityFeed/get_activity_feed_response.json')
        return activityFeedId
    
    # Retrieve activity_feed by configuration ID
    def get_activity_feedByConfigurationId(self, activity_feed_id):
        print("\n***************Sending GET request for get_activity_feedByConfigurationId********************")
        get_activity_feedByConfigurationId = "{}/edr/v2/activity-feed/configurations/{}".format(configfile.base_url, activity_feed_id)
        response = controller.callapirequest("Get_activity_feedByConfigurationId", "GET", get_activity_feedByConfigurationId, headers, False)        
        response_status = response.status_code
        print("\nStatus code received for get_activity_feedByConfigurationId: {}.\n\nResponse received for get_activity_feedByConfigurationId:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            if response.json()['meta']['totalResourceCount'] > 0:
                print("\nGET request for get-activity_feed By configuration ID is Successful")
            else:
                print("\nNo records found to validate the activity_feed functionality!!!")
        else:
            print("\nResponse error Status code for get_activity_feed is: {}".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/ActivityFeed/get_activity_feed_by_configuration_id_response.json')

    #Patch the activity_feed api
    def patch_activity_feed(self, activity_feed_id):
        with open('./payloads/ActivityFeed/patch_activity_feed.json') as json_path:
            activity_feed_payload = json_path.read()
        req_payload = json.loads(activity_feed_payload)
        req_payload["data"]["id"] = activity_feed_id
        activity_feed_url = "{}/edr/v2/activity-feed/configurations/{}".format(configfile.base_url, activity_feed_id)

        print("\n***************Sending PATCH request for patch_activity_feed********************")
        time.sleep(5)
        urllib3.disable_warnings()
        response = controller.callapirequest("Patch-activity_feed", "PATCH", activity_feed_url, headers, req_payload, False)
        response_status = response.status_code
        print("\nStatus code received for patch_activity_feed: {}.\n\nResponse received for patch_activity_feed:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            print("\nPatch Activity Feed request sent Successfully")
        else:
            print("\nResponse error status code for patch Activity Feed is: {}.".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/ActivityFeed/patch_activity_feed_response.json')
        
    # Delete activity feed by configuration ID
    def delete_activity_feedByConfigurationId(self, activity_feed_id):
        print("\n***************Sending DELETE request for delete_activity_feedByConfigurationId********************")
        delete_activity_feedByConfigurationId = "{}/edr/v2/activity-feed/configurations/{}".format(configfile.base_url, activity_feed_id)
        response = controller.callapirequest("Delete-activity_feedbyactivity_feedId", "DELETE", delete_activity_feedByConfigurationId, headers, False)        
        response_status = response.status_code
        print("\nStatus code received for delete_activity_feedByConfigurationId: {}.\n\nResponse received for delete_activity_feedByConfigurationId:\n\n{}".format(response_status, response.text))
        
        if response_status == 200:
            print("\nDELETE request for delete-activity_feed By activity_feed ID is Successful")
        else:
            print("\nResponse error Status code for delete_activity_feed is: {}".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/ActivityFeed/delete_activity_feed_by_configuration_id_response.json')

    #Delete activity feed by Tenant
    def delete_activity_feedByTenant(self):
        print("\n***************Sending DELETE request for delete_activity_feedByTenant********************")
        delete_activity_feedByTenant = "{}/edr/v2/activity-feed/tenant".format(configfile.base_url)
        response = controller.callapirequest("Delete-activity_feedbyactivity_feedId", "DELETE", delete_activity_feedByTenant, headers, False)        
        response_status = response.status_code
        print("\nStatus code received for delete_activity_feed_by_activity_feedId: {}.\n\nResponse received for delete_activity_feed_by_activity_feedId:\n\n{}".format(response_status, response.text))
        
        if response_status == 204:
            print("\nDELETE request for delete-activity_feed By activity_feed ID is Successful")
        else:
            print("\nResponse error Status code for delete_activity_feed is: {}".format(response_status))
            
        controller.write_responsetoFile(response.text, './results/ActivityFeed/delete_activity_feed_by_tenant_response.json')
      
def main():   
    #removing response json files before execution starts
    controller.remove_filesfromdir("./results/ActivityFeed") 
    obj_activity_feed = activity_feed()
    print("\n*********************START OF ACTIVITY FEED***********************")
    obj_activity_feed.post_activity_feed() # calling Post activity_feed API
    activity_feed_id = obj_activity_feed.get_activity_feed()   # calling get activity_feed API
    obj_activity_feed.patch_activity_feed(activity_feed_id) # calling Patch activity_feed API
    obj_activity_feed.get_activity_feedByConfigurationId(activity_feed_id)   # calling get activity_feed by configuration ID API
    obj_activity_feed.delete_activity_feedByConfigurationId(activity_feed_id) # calling delete activity_feed by configuration ID API
    obj_activity_feed.delete_activity_feedByTenant() # calling delete activity_feed by tenant
    print("\n*********************END OF ACTIVITY FEED**************************")

#Main Function    
if __name__=="__main__":
    main()