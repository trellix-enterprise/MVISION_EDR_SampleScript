import json
import requests
import time
import controller
import urllib3
import configfile

class Mvapi_ds(object):
    def ds_postrequest(self):
        global Auth_token
        global headers
        Auth_token= "Bearer {}".format(controller.get_token(configfile.client_userid, configfile.client_credentials))
        headers = {
            'x-api-key': configfile.x_api_key,
            'Authorization': Auth_token,
            'Content-Type': 'application/vnd.api+json'
        }
        var_dssearchid = ""
        with open('./payloads/Search/deviceSearch.json') as json_path:
            devicesearch_payload = json_path.read()
        req_payload = json.loads(devicesearch_payload)
        search_url = "{}/edr/v2/searches/historical".format(configfile.base_url)
        
        print("\n***************Sending POST request for Device Search********************")
        time.sleep(5)
        urllib3.disable_warnings()
        response = controller.callapirequest("Post-Devicesearch", "POST", search_url, headers, req_payload, False)        
        response_status = response.status_code
        print("\n Response received: {}".format(response.text))
        
        if response_status == 201:
            var_dssearchid = response.json()['data']['id']
        else:
            var_dssearchid = "0"
            print("\nResponse error status code for post Device search is: {}. Stopping Execution.".format(response_status))
            controller.write_responsetoFile(response.text, './results/Mvapi_ds/post_devicesearch_response.json')
            exit()
        controller.write_responsetoFile(response.text, './results/Mvapi_ds/post_devicesearch_response.json')
        return var_dssearchid
        
    def ds_getstatus(self, ds_searchid):
        status_url = "{}/edr/v2/searches/queue-jobs/{}".format(configfile.base_url, ds_searchid)
        time.sleep(5)
        print("\n***************Sending GET request for DS get_status********************")
        response = requests.get(status_url, headers=headers, allow_redirects=False)
        print("\n Response received: {}".format(response.text)) 
        response_status = response.status_code
        if response_status == 200:
            status = True
            retry = 0
            max_attempt = 5
            while status:
                if retry < max_attempt:
                    if requests.request("GET", status_url, headers=headers, allow_redirects=False).status_code!= 303:
                        print("Attempt_count {}".format(retry))
                        print("Status is inprogress,  sleep for 10 seconds")
                        time.sleep(10)
                        retry += 1
                        continue
                status = False
                break
        elif response_status == 303:
            print("\nStatus code for DS get status is {}".format(response_status))
        else:
            print("\nResponse error status code for DS get status is: {}. Stopping Execution.".format(response_status))
            exit()

    def ds_getresults(self, ds_searchid):
        result_url = "{}/edr/v2/searches/historical/{}/results?page[offset]=0&page[limit]=500".format(configfile.base_url,ds_searchid)
        time.sleep(5)
        print("\n***************Sending GET request for DS get_result********************")
        response = requests.request("GET", result_url, headers=headers)
        
        print("\nStatus code received for get_DSsearchresult: {}.\n\nResponse received for get_DSsearchresult\n\n{}".format(response.status_code, response.text))     
        controller.write_responsetoFile(response.text, './results/Mvapi_ds/ds_getresult_response.json')
       
        if response.status_code == 200 and len(response.json()["data"]) > 0:
            print("\n############### DeviceSearch Successful##########################")
        else:
            print("\n################# No data for DeviceSearch Query########################")
            
    def ds_getexport(self, ds_searchid):
        Export_result_url = "{}/edr/v2/searches/historical/{}/results?output=file&format=csv".format(configfile.base_url,ds_searchid)
        time.sleep(5)
        
        print("\n***************Sending GET request for DS get_exportfileurl********************")
        response = requests.request("GET", Export_result_url, headers=headers)
        response_dict = json.loads(response.text)
        file_url=response_dict['data']['attributes']['file_url']
        print("\nFile url: {}".format(file_url)) 
        controller.write_responsetoFile(response.text, './results/Mvapi_ds/ds_exportfile_url_response.json')
            
def main(): 
    #removing response json files before execution starts
    controller.remove_filesfromdir("./results/Mvapi_ds")   
    obj_mvapids =  Mvapi_ds()
    print("\n*********************START OF DEVICE SEARCH**************************")
    ds_searchid = obj_mvapids.ds_postrequest()
    obj_mvapids.ds_getstatus(ds_searchid)
    obj_mvapids.ds_getresults(ds_searchid)
    obj_mvapids.ds_getexport(ds_searchid)
    print("\n*********************END OF DEVICE SEARCH**************************")        

if __name__=="__main__":
    main()