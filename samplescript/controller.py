import requests
import json
import urllib3
import configfile
import os
import time

# Function to generate Authentication token
# input: client_userid and client_credentials to be read from configfile.py
# output: returns authentication token
def get_token(client_userid, client_credentials):
    token = " "
    print("\n***********************GENERATING IAM TOKEN*************************")
    urllib3.disable_warnings()
    params = {'grant_type': configfile.grant_type,'scope' : configfile.scope}   
    response = requests.get(configfile.iam_url, timeout=60, verify=False, params=params , auth=(client_userid, client_credentials))
    
    if 'access_token' in json.loads(response.content):
        token = json.loads(response.content).get('access_token')
        print("\n***********************IAM TOKEN GENERATED***********************")
    else:
        print("\n************IAM TOKEN GENERATION FAILED.EXITING...****************")
        exit()
    return token    

# Function to write the Json response to mentioned file path
# input: response of the API request, file path where response to be written
# output: NA
def write_responsetoFile(response, filepath):
    with open(filepath, "w") as outfile:
        json.dump(response, outfile)

# Function to delete all files from mentioned file path 
# input: full directory path where files to be removed
# output: NA
def remove_filesfromdir(dir_path):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('\nFailed to delete %s. Reason: %s' % (file_path, e))

# Function to retry calling the API after mentioned time while there is a 429 error receied
# input: response of the API request
# output: returns retry interval in secs while there is an 429 error
def get_retryinterval(response):
    print("\nResponse Header received:\n\n{}".format(response.headers))
    retry_val = "0"
    if 'Retry-After' in response.headers:
        retry_val = response.headers["Retry-After"]
        retry_val = retry_val[:-1]
        print('\nRetry interval set to {} secs. Sleeping...'.format(retry_val))
    else:
        print("\nRetry-after attribute is not present in response header..")
    return retry_val

# Function to call the POST and GET request. It will retry once only if there is a 429 status code returned in response
# input: API name, Method name(POST/GET), API Url , headers, Payload for POST request, verify
# output: returns the response of the POST/GET request made for the respective API
def callapirequest(apiname, method, urlpath, headerreq, req_payload=None, verify=False):
    if method == "POST":
        response = requests.post(urlpath, headers=headerreq, data=json.dumps(req_payload), verify=False)
        response_status = response.status_code
        if(response_status == 429):
            print("\nResponse code received as 429 for {}, Retry the request after mentioned interval".format(apiname))
            retry_interval = int(get_retryinterval(response))
            if  retry_interval != 0:
                time.sleep(retry_interval)
                print("\nRetrying the {} API request after {} secs.".format(apiname, retry_interval))
                response = requests.post(urlpath, headers=headerreq, data=json.dumps(req_payload), verify=False)
        return response   
    elif method == "GET":
        response = requests.get(urlpath, headers=headerreq, verify=False)
        response_status = response.status_code
        if(response_status == 429):
            print("\nResponse code received as 429 for {}, Retry the request after mentioned interval".format(apiname))
            retry_interval = int(get_retryinterval(response))
            if  retry_interval != 0:
                time.sleep(retry_interval)
                print("\nRetrying the {} API request after {} secs.".format(apiname, retry_interval))
                response = requests.get(urlpath, headers=headerreq, verify=False)
        return response 
    elif method == "DELETE":
        response = requests.delete(urlpath, headers=headerreq, verify=False)
        response_status = response.status_code
        if(response_status == 429):
            print("\nResponse code received as 429 for {}, Retry the request after mentioned interval".format(apiname))
            retry_interval = int(get_retryinterval(response))
            if  retry_interval != 0:
                time.sleep(retry_interval)
                print("\nRetrying the {} API request after {} secs.".format(apiname, retry_interval))
                response = requests.delete(urlpath, headers=headerreq, verify=False)
        return response
    elif method == 'PATCH':
        response = requests.patch(urlpath, headers=headerreq, data=json.dumps(req_payload), verify=False)
        response_status = response.status_code
        if(response_status == 429):
            print("\nResponse code received as 429 for {}, Retry the request after mentioned interval".format(apiname))
            retry_interval = int(get_retryinterval(response))
            if  retry_interval != 0:
                time.sleep(retry_interval)
                print("\nRetrying the {} API request after {} secs.".format(apiname, retry_interval))
                response = requests.patch(urlpath, headers=headerreq, data=json.dumps(req_payload), verify=False)
        return response
    else:
        print("API call method is set to other than GET and POST. Stopping Execution...")
        exit()

         
