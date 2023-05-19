pre-requisite:
- install python2.7
- pip install requests

swms details:

projections folder:
- Contains request payloads for respective POST API calls 

results folder:
- Contains response from the API calls 


configfile.py : 
controller.py : contains tenant credentials [to be updated by the customer] before token generation
host_remediation.py : contains the complete flow for host based remediation.
search_remediation.py : contains the complete flow for search based remediation.
action_history.py :
get_evidence.py :
get_investigation.py : 
get_metadata.py : 
get_threats.py : 

Steps to run:
1. change the config file as required
1. Update the tenant details for token generationand host_name for hostbased remediation in controller.py 
2. python <file_name.py>
Note: Python 2.7 is the verified version on which the code was successfully executed.

------------------------
Host Based Remediation:
-------------------------
action : [QuarantineHost , UnquarantineHost]

-----------------------------
Search Based Remediation
-----------------------------
action : [QuarantineHost, UnquarantineHost, deleteFolder, removeFile, removeFileSafe, deleteRegistryValue, stopAndRemoveContent, stopAndRemoveFile, killProcess, killProcessByName, killProcessByPath, killProcessByHash, killProcessTree, executeRebootOperatingSystem, executeUserLogoff]
actionInputs->name : [full_path, full_name, keypath, keyvalue, pid, name, sha256, sha1, md5, kill_tree, username]
