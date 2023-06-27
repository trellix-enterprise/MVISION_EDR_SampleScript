import json
import requests
import time
import controller
import urllib3
import configfile

class Mvapi_hs(object):
    def hs_postrequest(self):
        global Auth_token
        global headers
        Auth_token= "Bearer {}".format(controller.get_token(configfile.client_userid, configfile.client_credentials))
        headers = {
            'x-api-key': configfile.x_api_key,
            'Authorization': Auth_token,
            'Content-Type': 'application/vnd.api+json'
        }
        var_hssearchid = ""
        with open('./payloads/Search/HS_projection.json') as json_path:
            historicalsearch_payload = json_path.read()
        req_payload = json.loads(historicalsearch_payload)
        search_url = "{}/edr/v2/searches/historical".format(configfile.base_url)
        
        print("\n***************Sending POST request for Historical Search********************")
        time.sleep(5)
        urllib3.disable_warnings()
        response = requests.post(search_url, headers=headers, data=req_payload)        
        response_status = response.status_code
        
        if response_status == 201:
            var_hssearchid = response.json()['data']['id']
        else:
            var_hssearchid = "0"
            print("\nResponse error status code for post Historical search is: {}. Stopping Execution.".format(response_status))
            controller.write_responsetoFile(response.text, './results/Mvapi_hs/post_historicalserach_response.json')
            exit()
        controller.write_responsetoFile(response.text, './results/Mvapi_hs/post_historicalserach_response.json')
        return var_hssearchid
        
    def hs_getstatus(self, hs_searchid):
        status_url = "{}/edr/v2/searches/queue-jobs/{}".format(configfile.base_url, hs_searchid)
        time.sleep(5)
        print("{}{}".format(status_url,headers))
        response = requests.get(status_url, headers=headers)
        response_status = response.status_code
        if response_status == 200:
            status = True
            retry = 0
            max_attempt = 5
            while status:
                if retry < max_attempt:
                    if requests.request("GET", status_url, headers=headers).status_code!= 303:
                        print("Attempt_count {}".format(retry))
                        print("Status is inprogress,  sleep for 10 seconds")
                        time.sleep(10)
                        retry += 1
                        continue
                status = False
                break
        else:
            print("\nResponse error status code for RTS get status is: {}. Stopping Execution.".format(response_status.status_code))
            exit()

    def hs_getresults(self, hs_searchid):
        result_url = "{}/edr/v2/searches/historical/{}/results?page[offset]=0&page[limit]=500".format(configfile.base_url,hs_searchid)
        print(result_url)
        time.sleep(5)
        response = requests.request("GET", result_url, headers=headers)
        print("\nStatus code received for get_RTSsearchresult: {}.\n\nResponse received for get_RTSsearchresult\n\n{}".format(response.status_code, response.text))     
        controller.write_responsetoFile(response.text, './results/Mvapi_hs/hs_getresult_response.json')
       
        if response.status_code == 200 and len(response.json()["data"]) > 0:
            print("Search Successful")
        else:
            print("No data for Search Query")
            
    def hs_getexport(self, hs_searchid):
        Export_result_url = "{}/edr/v2/searches/historical/{}/results?output=file&format=csv".format(configfile.base_url,hs_searchid)
        print(Export_result_url)
        time.sleep(5)
        response = requests.request("GET", Export_result_url, headers=headers)
        
        controller.write_responsetoFile(response.text, './results/Mvapi_hs/hs_exportfile_url_response.json')
        
            
    def main(): 
    #removing response json files before execution starts
        controller.remove_filesfromdir("./results/Mvapi_hs")   
        obj_mvapids =  Mvapi_hs()
        print("\n*********************START OF HISTORICAL SEARCH**************************")
        hs_searchid = obj_mvapids.hs_postrequest()
        obj_mvapids.hs_getstatus(hs_searchid)
        obj_mvapids.hs_getresults(hs_searchid)
        obj_mvapids.hs_getexport(hs_searchid)
        print("\n*********************END OF HISTORICAL SEARCH**************************")        

    if __name__=="__main__":
        main()