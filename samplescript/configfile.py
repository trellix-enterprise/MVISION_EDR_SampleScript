# Required URLS 
base_url = 'https://us-west-2-api-inteks-ls.mvisionapiedr.net'
iam_url='https://preprod.iam.mcafee-cloud.com/iam/v1.0/token'

#Headers to be included
x_api_key="ECYPmTx9g01rWmT3TXUTs8mNkHjbaNSv7lAp6uov"
grant_type = "client_credentials"
scope = "epo.admin mi.user.config mi.user.investigate gsd.a.e soc.rts.c soc.rts.r soc.hts.c soc.hts.r soc.act.tg"

# User to update tenant credentials
client_userid="Z3C5ke6wQeVFnC-0LLSDmgHM6" #"test3132334@yopmail.com" #"test2122234@yopmail.com"
client_credentials="wF-EJpHq73FQm1mmhNzC399D1" 
# For get-threat API please use below tenant as threats are present here
gtclient_id="Z3C5ke6wQeVFnC-0LLSDmgHM6"
gtclient_credentials="wF-EJpHq73FQm1mmhNzC399D1" 
# User to update the host machine name for hostbased remediation
host_name = "DESKTOP-BUV2HRF"#DESKTOP-2HS9OV4"

#For Exclusions api
# client_id_auth="0oae6vfj6gCEIsMId0h7"
# grant_type_auth = "password"
# gtclient_id_auth="vasav-lowerint-3@yopmail.com"
# gtclient_credentials_auth="Mcafee@123" 

#Variables used to be read and modify from here
rts_query_name = "ProcessHistory"
searchrem_action_name = "killProcessByName"
searchrem_action_input_name = "full_name"
searchrem_action_input_value = "mfemvedr"

actionhistory_offset = 0
actionhistory_pagelimit = 20
actionhistory_sort = "status"

getthreats_offset = 0
getthreats_pagelimit = 20
getthreats_from = 9999
getthreats_sort = "firstDetected"

alerts_from = 1683549043263
alerts_filter ="%7B%22severities%22%3A%20%5B%20%22s0%22%2C%20%22s1%22%2C%20%22s2%22%2C%20%22s3%22%2C%20%22s4%22%2C%20%22s5%22%20%5D%20%7D"

