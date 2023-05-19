import logging
import json
import requests
import time
from requests.models import Response
import controller
import urllib3
import configfile

class action_history(object):
    # Get the actions history result
    # API response is written into  ./results/ActionHistory/get_actionhistory_response.json file
    def get_actionhistory(self):
        global Auth_token
        global headers
        #Generate Authentication Token, change the client_userid and client_credentials in configfile.py
        Auth_token= "Bearer {}".format(controller.get_token(configfile.client_userid, configfile.client_credentials))
        headers = {
            'x-api-key': configfile.x_api_key,
            'Authorization': Auth_token,
            'Content-Type': 'application/vnd.api+json'
        }        
        print("\n***************Sending GET request for action_history********************")
        #To create the URL, make necessary changes in  configfile.py
        actionhistory_url = "{}/edr/v2/remediation/actions?page[offset]={}&page[limit]={}&sort={}".format(configfile.base_url, configfile.actionhistory_offset, configfile.actionhistory_pagelimit, configfile.actionhistory_sort)
        print("Action History URL is : {}".format(actionhistory_url))
        #call the get method for actionhistory api
        response = controller.callapirequest("Action_History", "GET", actionhistory_url, headers, False)        
        response_status = response.status_code
        print("\nStatus code received for Action History API: {}.\n\nResponse received for get_actionhistory:\n\n{}".format(response_status, response.text))
        if response_status == 200:
            if response.json()['meta']['totalResourceCount'] != 0:
                print("\nGET request for Action History fetched {} records".format( response.json()['meta']['totalResourceCount']))
            else:
                print("\nNo records found to validate the action-history functionality!!!")
        else:
            print("\nResponse error Status code for get_actionhistory is: {}".format(response_status))
            
        # Write the response Json to /results/ActionHistory/get_actionhistory_response.json file
        controller.write_responsetoFile(response.text, './results/ActionHistory/get_actionhistory_response.json')
      
def main():   
    #removing response json files before execution starts
    controller.remove_filesfromdir("./results/ActionHistory") 
    obj_actionhistory =  action_history()
    print("\n*********************START OF ACTION HISTORY***********************")
    res = obj_actionhistory.get_actionhistory()   # calling get action history API
    print("\n*********************END OF ACTION HISTORY**************************")

#Main Function    
if __name__=="__main__":
    main()