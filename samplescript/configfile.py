# Required URLS 
base_url = 'https://us-west-2-api-inteks-ls.mvisionapiedr.net'
iam_url='https://preprod.iam.mcafee-cloud.com/iam/v1.0/token'

#Headers to be included
x_api_key="ECYPmTx9g01rWmT3TXUTs8mNkHjbaNSv7lAp6uov"
client_id="0oae6vfj6gCEIsMId0h7"
grant_type = "password"
scope = "epo.admin mi.user.config mi.user.investigate gsd.a.e soc.rts.c soc.rts.r soc.hts.c soc.hts.r soc.act.tg"

# User to update tenant credentials
client_userid="test2122234@yopmail.com" #"test3132334@yopmail.com" #"test2122234@yopmail.com"
client_credentials="Trellix@1234" 
# For get-threat API please use below tenant as threats are present here
gtclient_id="vasav-lowerint-3@yopmail.com"
gtclient_credentials="Mcafee@123" 
# User to update the host machine name for hostbased remediation
host_name = "DESKTOP-BUV2HRF"#DESKTOP-2HS9OV4"

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
