import json
import requests
import time
import controller
import urllib3
import configfile

class Mvapi_rts(object):
    def rts_postrequest(self):
        global Auth_token
        global headers
        Auth_token= "Bearer {}".format(controller.get_token(configfile.client_userid, configfile.client_credentials))
        headers = {
            'x-api-key': configfile.x_api_key,
            'Authorization': Auth_token,
            'Content-Type': 'application/vnd.api+json'
        }
        var_rtssearchid = ""
        with open('./payloads/Search/realtimeSearch.json') as json_path:
            realtimesearch_payload = json_path.read()
        req_payload = json.loads(realtimesearch_payload)
        search_url = "{}/edr/v2/searches/realtime".format(configfile.base_url)
        
        print("\n***************Sending POST request for Real Time Search********************")
        time.sleep(10)
        urllib3.disable_warnings()
        response = controller.callapirequest("Post-Realtimesearch", "POST", search_url, headers, req_payload, False)        
        response_status = response.status_code
        print("\n Response received: {}".format(response.text))
        if response_status == 201:
            var_rtssearchid = response.json()['data']['id']
        else:
            var_rtssearchid = "0"
            print("\nResponse error status code for post Real time search is: {}. Stopping Execution.".format(response_status))
            controller.write_responsetoFile(response.text, './results/Mvapi_rts/post_realtimeserach_response.json')
            exit()
        controller.write_responsetoFile(response.text, './results/Mvapi_rts/post_realtimeserach_response.json')
        return var_rtssearchid
        
    def rts_getstatus(self, rts_searchid):
        status_url = "{}/edr/v2/searches/queue-jobs/{}".format(configfile.base_url, rts_searchid)
        time.sleep(10)
        print("\n***************Sending GET request for RTS get_status********************")
        response = requests.request("GET", status_url, headers=headers, allow_redirects=False)
        response_status = response.status_code
        if response_status == 200:
            status = True
            retry = 0
            max_attempt = 10
            while status:
                if retry < max_attempt:
                    if requests.request("GET", status_url, headers=headers, allow_redirects=False).status_code!= 303:
                        print("Attempt_count {}".format(retry))
                        print("Status is inprogress, sleep for 15 seconds")
                        time.sleep(15)
                        retry += 1
                        continue
                status = False
                break
        elif response_status == 303:
            print("\nStatus code for RTS get status is {}".format(response_status))
        else:
            print("\nResponse error status code for RTS get status is: {}. Stopping Execution.".format(response_status))
            exit()

    def rts_getresults(self, rts_searchid):
        print("\n***************Sending GET request for RTS get_result********************")
        result_url = "{}/edr/v2/searches/realtime/{}/results?page[offset]=0&page[limit]=500".format(configfile.base_url,rts_searchid)
        time.sleep(5)
        response = requests.request("GET", result_url, headers=headers)
        print("\nStatus code received for get_RTSsearchresult: {}.\n\nResponse received for get_RTSsearchresult\n\n{}".format(response.status_code, response.text))     
        controller.write_responsetoFile(response.text, './results/Mvapi_rts/rts_getresult_response.json')
       
        if response.status_code == 200 and len(response.json()["data"]) > 0:
            print("\n###############RealtimeSearch Successful##########################")
        else:
            print("\n#################No data for RealtimeSearch Query########################")
            
    def rts_getexport(self, rts_searchid):
        Export_result_url = "{}/edr/v2/searches/realtime/{}/results?output=file&format=csv".format(configfile.base_url,rts_searchid)
        time.sleep(5)
        print("\n***************Sending GET request for RTS get_exportfileurl********************")
        response = requests.request("GET", Export_result_url, headers=headers)
        response_dict = json.loads(response.text)
        file_url=response_dict['data']['attributes']['file_url']
        print("\nFile url: {}".format(file_url))
        controller.write_responsetoFile(response.text, './results/Mvapi_rts/rts_exportfile_url_response.json')  
            
def main(): 
#removing response json files before execution starts
    controller.remove_filesfromdir("./results/Mvapi_rts")   
    obj_mvapirts =  Mvapi_rts()
    print("\n*********************START OF REALTIME SEARCH**************************")
    rts_searchid = obj_mvapirts.rts_postrequest()
    obj_mvapirts.rts_getstatus(rts_searchid)
    obj_mvapirts.rts_getresults(rts_searchid)
    obj_mvapirts.rts_getexport(rts_searchid)
    print("\n*********************END OF REALTIME SEARCH*****************************")        

if __name__=="__main__":
    main()