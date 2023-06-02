import logging
import json
import requests
import time
from requests.models import Response
import controller
import urllib3
import configfile

class alerts(object):
    # Get the aleting api result
    # API response is written into  ./results/Alerts/get_alerts_response.json file
    def get_alerts(self):
        global Auth_token
        global headers
        #Generate Authentication Token, change the client_userid and client_credentials in configfile.py
        Auth_token= "Bearer {}".format(controller.get_token(configfile.client_userid, configfile.client_credentials))
        headers = {
            'x-api-key': configfile.x_api_key,
            'Authorization': Auth_token,
            'Content-Type': 'application/vnd.api+json'
        }        
        print("\n***************Sending GET request for alerts********************")
        #To create the URL, make necessary changes in  configfile.py
        alert_url = "{}/edr/v2/alerts?from={}&filter={}".format(configfile.base_url,configfile.alerts_from, configfile.alerts_filter)
        print("Alerting URL is : {}".format(alert_url))
        #call the get method for alerting api
        response = controller.callapirequest("Alerting", "GET", alert_url, headers, False)        
        response_status = response.status_code
        print("\nStatus code received for Alerting API: {}.\n\nResponse received for get_alerts:\n\n{}".format(response_status, response.text))
        if response_status == 200:
            if response.json()['meta']['totalResourceCount'] != 0:
                print("\nGET request for Alerts fetched {} records".format( response.json()['meta']['totalResourceCount']))
            else:
                print("\nNo records found to validate the alerting functionality!!!")
        else:
            print("\nResponse error Status code for get_alerts is: {}".format(response_status))
            
        # Write the response Json to /results/ActionHistory/get_actionhistory_response.json file
        controller.write_responsetoFile(response.text, './results/Alerts/get_alerts_response.json')
      
def main():   
    #removing response json files before execution starts
    controller.remove_filesfromdir("./results/Alerts") 
    obj_alerts = alerts()
    print("\n*********************START OF ALERTS***********************")
    obj_alerts.get_alerts()   # calling get alerts API
    print("\n*********************END OF ALERTS**************************")

#Main Function    
if __name__=="__main__":
    main()