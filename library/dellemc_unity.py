#!/usr/bin/python

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = ''' 
---
module: dellemc_unity
short_description: Configure and manage Dell EMC Unity Storage System
description:
    - This module can be use d to configure and manage Dell EMC Unity Storage System.
    - The module supports check mode.
version_added: "2.2"
author: 
    - "Jiale Huo (jiale.huo@emc.com)"
    - "Craig Smith (craig.j.smith@emc.com)"
options:
    unity_hostname:
        description: 
            - Hostname of the Unity system's management interface.
        required: true 
        type: string
    unity_username:
        description: 
            - Username of the Unity system's default administrator user.
        required: false
        default: "admin"
        type: string
    unity_password:
        description: 
            - Password of the Unity system's default administrator user.
        required: false
        default: "Password123#"
        type: string
    unity_accept_eula:
        description:
            - Indicate whether the administrator accepts the EULA of the Unity system.
        required: false
        default: False
        type: bool
    unity_new_password:
        description: 
            - New password to replace the old one of the Unity system's default administrator user.
        required: false
        type: string
    unity_license_path:
        description:
            - Path to the license file of the Unity system.
        required: false
        type: string
    unity_other_users:
        description:
            - Create or update users of the Unity system other than the default administrator user.
        required: false
        type: list
        suboptions:
            username: 
                description:
                    - Username of the user.
                required: true
                type: string
            password:
                description:
                    - Password of the user.
                required: true
                type: string
            new_password:
                description:
                    - New password to replace the old one of the user.
                required: false
                type: string
            role:
                description:
                    - Role of the user in the Unity system.
                required: false
                default: "administrator"
                choices:
                    - administrator
                    - operator
                    - storageadmin
                    - vmadmin
                type: string
    unity_dns_servers:
        description:
            - Update DNS servers of the Unity system.
        required: false
        type: list
    unity_ntp_servers:
        description:
            - Update NTP servers of the Unity system.
        required: false
        type: list
    unity_ntp_reboot_privilege:
        description:
            - Option to reboot the Unity system when updating NTP servers.
            - Reboot for a time change is required only if the time shift exceeds a threshold of 1000 seconds. 
            - If a reboot is required, and allowed, on a single SP system or a system with only one SP operating, then clients will be unable to access data during the reboot. 
        required: false
        default: 0
        choices:
            - 0 = No_Reboot_Allowed: Set time or NTP server if possible without a reboot.
            - 1 = Reboot_Allowed: Set time or NTP server if possible; reboot if needed, but do not allow data unavailability.
            - 2 = DU_Allowed: Set time or NTP server if possible; reboot if needed, even if this will cause data unavailability.
        type: int
    unity_queries:
        description:
            - Query the Unity system for resource information.
            - See "Unisphere Management REST API Programmer's Guide" for detailed description and examples of the query parameters.
        required: false
        type: list
        suboptions:
            resource_type: 
                description:
                    - Type of the resource to be queried.
                required: true
                type: string
            id:
                description:
                    - ID of an instance of the resouce type to be queried.
                    - If this option is missing, then collection query of the resource type will be executed.
                    - Otherwise, if this option is present, then instance query of the resource type will be executed. 
                required: false
                type: string
            compact:
                description:
                    - Omits metadata from each instance in the query response.
                required: false
                default: true
                type: bool
            fields:
                description:
                    - Specifies a comma-separated list of attributes to return in a response. 
                    - If you do not use this parameter, a query will return the id attribute only.
                    - When using fields, you can:
                        - Use dot notation syntax to return the values of related attributes.
                        - Optionally, define a new attribute from field expressions associated with one or more existing attributes.
                required: false
                type: string
            filter:
                description:
                    - Filters the response data against a set of criteria. Only matching resource instances are returned. Filtering is case insensitive.
                    - When using filter, you can use dot notation syntax to filter by the attributes of related resource types.
                    - Only applies to collection query requests.
                required: false
                type: string
            groupby:
                description:
                    - Groups the specified values and applies the @sum function to each group.
                    - For example, you could use groupby with @sum to return a summary of disk sizes for each disk type.
                    - Only applies to collection query requests.
                required: false
                type: string
            language:
                description:
                    - Overrides the value of the Accept-language: header.
                    - This is useful for testing from a plain browser or from an environment where URL parameters are easier to use than HTTP headers.
                    - The language parameter specifies the localization language for error messages, events, alerts, and other localizable responses.
                required: false
                choices:
                    - de-DE: German
                    - en-US: English 
                    - es-MX: Latin American Spanish
                    - fr-FR: French
                    - ja-JP: Japanese
                    - ko-KR: Korean
                    - pt-BR: Brazilian Portuguese
                    - ru-RU: Russian
                    - zh-CN: Chinese
                default: en-US
                type: string
            orderby:
                description:
                    - Specifies how to sort response data. You can sort response data in ascending or descending order by the attributes of the queried resource type. And you can use dot notation syntax to sort response data by the attributes of related resource types.
                    - Only applies to collection query requests.
                required: false
                type: string
            page:
                description:
                    - Identifies the page to return in a response by specifying the page number. If this parameter is not specified, the server returns all resource instances that meet the request criteria in page 1.
                    - Only applies to collection query requests.
                required: false
                type: int
            per_page:
                description:
                    - Specifies the number of resource type instances that form a page. If this parameter is not specified, the server returns all resource instances that meet the request criteria in the page specified by page (or in page 1, if page is also not specified).
                    - The server imposes an upper limit of 2000 on the number of resource instances returned in a page.
                    - Only applies to collection query requests.
                required: false
                type: int
            with_entrycount:
                description:
                    - Indicates whether to return the entryCount response component in the response data. The entryCount response component indicates the number of resource instances in the complete list. You can use it to get the total number of entries when paging returned a partial response.
                    - By default, the entryCount response component is not returned. Set with_entrycount=true to return the entryCount response component.
                    - Only applies to collection query requests.
                required: false
                default: true
                type: bool
notes:
    - GitHub project: U(https://github.com/jialehuo/ansible-dellemc-unity)
    - This module supports check mode.
requirements:
    - Python >= 2.7
    - requests >= 1.3
    - Unity >= 4.0
'''

EXAMPLES = '''
- name: Initial setup
  dellemc_unity:
    unity_hostname: "192.168.0.100"
    unity_username: admin
    unity_password: Password123#
    unity_accept_eula: true
    unity_new_password: Password123!
    unity_license_path: /home/labadmin/unity.lic
    unity_other_users:
      - {username: test1, password: Welcome1!} 
      - {username: test2, password: Welcome1!, role: operator}
    unity_dns_servers:
      - 10.10.0.21
      - 10.10.0.22
    unity_ntp_servers:
      - 0.pool.ntp.org
      - 1.pool.ntp.org
    unity_ntp_reboot_privilege: 2

- name: Update user password
  dellemc_unity:
    unity_hostname: "192.168.0.100"
    unity_password: Password123!
    unity_other_users:
      - {username: test1, password: Welcome1!, new_password: Welcome123!} 

- name: Query DNS and NTP server settings
  dellemc_unity:
    unity_hostname: "192.168.0.100"
    unity_password: Password123!
    unity_queries:
        - {resource_type: dnsServer, fields: "domain, addresses, origin", page: 1, per_page: 100}
        - {resource_type: ntpServer, id: "0", fields: addresses}
'''

RETURN = '''
unity_update_results:
    description: 
        - A list of JSON objects detailing the results of each successful update operation.
    returned: always
    type: list
    sample: >
        "unity_query_results": [
            {
                "entries": [
                    {
                        "content": {
                            "addresses": [
                                "10.254.66.23", 
                                "10.254.66.24"
                            ], 
                            "id": "0", 
                            "origin": 2
                        }
                    }
                ], 
                "entryCount": 1, 
                "resource_type": "dnsServer"
            }, 
            {
                "entries": [
                    {
                        "content": {
                            "addresses": [], 
                            "id": "0"
                        }
                    }
                ], 
                "entryCount": 1, 
                "resource_type": "ntpServer"
            }
        ]
    contains:
        entries:
            description:
                - A list of JSON objects for each instance of the resource type returned by the query.
            returned: always
            type: complex
            contains:
                content:
                    description: 
                        - Content of the instance.
                        - Contains at least the ID of the instance, and possibly other fields specified by the 'fields' parameter in the 'unity_queries' option.
                    returned: always
                    type: complex
        entryCount:
            description:
                - Count of entries returned.
            type: int
        resourceType:
            description:
                - Type of the resource returned.
            returned: always
            type: string

unity_query_results:
    description: 
        - A list of JSON objects detailing the results of each successful query operation.
    returned: always
    type: list
    sample: >
        "unity_update_results": [
            {
                "changed": {
                    "args": {
                        "isEulaAccepted": "true"
                    }, 
                    "url": "/api/instances/system/0/action/modify"
                }
            }, 
            {
                "changed": {
                    "args": {
                        "oldPassword": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER", 
                        "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"
                    }, 
                    "url": "/api/instances/user/user_admin/action/modify"
                }
            }, 
            {
                "ANTIVIRUS_license_update": "version 0 to version 1"
            }, 
            {
                "BASE_OE_V4_0_license_update": "version 0 to version 1"
            }, 
            {
                "CIFS_license_update": "version 0 to version 1"
            }, 
            {
                "ESA_ADAPTER_license_update": "version 0 to version 1"
            }, 
            {
                "FAST_VP_license_update": "version 0 to version 1"
            }, 
            {
                "ISCSI_license_update": "version 0 to version 1"
            }, 
            {
                "LOCAL_COPIES_license_update": "version 0 to version 1"
            }, 
            {
                "NFS_license_update": "version 0 to version 1"
            }, 
            {
                "QUALITY_OF_SERVICE_license_update": "version 0 to version 1"
            }, 
            {
                "THIN_PROVISIONING_license_update": "version 0 to version 1"
            }, 
            {
                "UNISPHERE_license_update": "version 0 to version 1"
            }, 
            {
                "UNISPHERE_CENTRAL_license_update": "version 0 to version 1"
            }, 
            {
                "changed": {
                    "args": {
                        "licensePath": "/home/labadmin/unity.lic"
                    }, 
                    "url": "https://192.168.0.202/upload/license"
                }
            }, 
            {
                "changed": {
                    "args": {
                        "name": "test1", 
                        "password": "Welcome1!", 
                        "role": "administrator"
                    }, 
                    "url": "/api/types/user/instances"
                }
            }, 
            {
                "changed": {
                    "args": {
                        "name": "test2", 
                        "password": "Welcome1!", 
                        "role": "operator"
                    }, 
                    "url": "/api/types/user/instances"
                }
            }, 
            {
                "changed": {
                    "args": {
                        "name": "test3", 
                        "password": "Welcome1!", 
                        "role": "administrator"
                    }, 
                    "url": "/api/types/user/instances"
                }
            }, 
            {
                "changed": {
                    "args": {
                        "oldPassword": "Welcome1!", 
                        "password": "Welcome1#"
                    }, 
                    "url": "/api/instances/user/user_test3/action/modify"
                }
            }, 
            {
                "changed": {
                    "args": {
                        "addresses": [
                            "10.254.66.25", 
                            "10.254.66.26"
                        ]
                    }, 
                    "url": "/api/instances/dnsServer/0/action/modify"
                }
            }, 
            {
                "changed": {
                    "args": {
                        "addresses": [
                            "10.254.140.21", 
                            "10.254.140.22"
                        ], 
                        "rebootPrivilege": 2
                    }, 
                    "url": "/api/instances/ntpServer/0/action/modify"
                }
            }
        ]
    contains:
        changed:
            description:
                - Resources changed in the Unity system.
                - Returned under non-check mode.
            type: complex
            contains:
                url:
                    description:
                        - URL of the operation to change the resource.
                    returned: always
                    type: string
                args:
                    description:
                        - Arguments of the operation to change the resource.
                    returned: always
                    type: complex
        to_be_changed:
            description:
                - Resources to be changed in the Unity system.
                - Returned under check mode.
            type: complex
            contains:
                url:
                    description:
                        - URL of the operation to change the resource.
                    returned: always
                    type: string
                args:
                    description:
                        - Arguments of the operation to change the resource.
                    returned: always
                    type: complex

'''

import requests, json, re
from ansible.module_utils.basic import AnsibleModule

class Unity:

  def __init__(self, module):
    self.hostname = module.params['unity_hostname']
    self.username = module.params['unity_username']
    self.password = module.params['unity_password']
    self.acceptEula = module.params['unity_accept_eula']
    self.newPassword = module.params['unity_new_password']
    self.licensePath = module.params['unity_license_path']
    self.otherUsers = module.params['unity_other_users']
    self.dnsServers = module.params['unity_dns_servers']
    self.ntpServers = module.params['unity_ntp_servers']
    self.ntpRebootPrivilege = module.params['unity_ntp_reboot_privilege']
    self.queries = module.params['unity_queries']

    self.checkMode = module.check_mode

    self.processedUsers = []
    self.apibase = 'https://' + self.hostname	# Base URL of the REST API
    self.headers = {'X-EMC-REST-CLIENT': 'true', 'content-type': 'application/json', 'Accept': 'application/json'}       # HTTP headers for REST API requests, less the 'EMC-CSRF-TOKEN' header
    self.session = requests.Session()
    self.changed = False
    self.updateResults = []
    self.queryResults = []
    self.err = None

  def _getMsg(self, resp):
    try:
      msg = json.loads(resp.text)
    except ValueError:
      msg = {'httpStatusCode': resp.status_code, 'messages': [{'en-US': resp.text}]}
    return msg

  def _getResult(self, resp):
    if resp.status_code // 100 == 2:	# HTTP status code 2xx = success
      pass
    else:
      self.err = self._getMsg(resp)
    return resp

  def _postResult(self, resp, url, args, changed=True):
    changedTxt = 'changed'
    if self.checkMode:
      changedTxt = 'to_be_changed'

    if self.checkMode or (resp and resp.status_code // 100 == 2):
      if changed:
        self.changed = changed
        self.updateResults.append({changedTxt: {'url': url, 'args': args}})
    else:
      self.err = self._getMsg(resp)
      self.err.update({'url': url, 'args': args})

  def _doPost(self, url, args, changed=True):
    if self.checkMode:
      resp = None
    else:
      resp = self.session.post(self.apibase + url, json = args, headers=self.headers, verify=False)
    self._postResult(resp, url, args, changed=changed)

  def _doGet(self, url, params):
    return self._getResult(self.session.get(self.apibase + url, params=params, headers=self.headers, verify=False))

  def processAuthResult(self, resp, username):
    self._getResult(resp)
    if self.err: 	
      if resp.status_code == 401:	# Unauthorized password
        self.err['messages'][0]['en-US'] = "Authentication error for User '" + username + "'" 	# Update error message
    return resp

  def startSession(self):
    resp = self.session.get(self.apibase+'/api/instances/system/0', auth=requests.auth.HTTPBasicAuth(self.username, self.password), headers=self.headers, verify=False)
    self.processAuthResult(resp, self.username)
    if resp.status_code // 100 == 2:	# 2xx status code - success
      # Add 'EMC-CSRF-TOKEN' header
      self.headers['EMC-CSRF-TOKEN']=resp.headers['EMC-CSRF-TOKEN']

  def stopSession(self):
    url = '/api/types/loginSessionInfo/action/logout'
    args = {'localCleanupOnly' : 'true'}
    self._doPost(url, args, changed=False)

  def acceptEULA(self):
    url = '/api/instances/system/0'
    params = {'fields':'isEULAAccepted'}
    resp = self._doGet(url, params)
    if resp.status_code // 100 == 2:
      if not json.loads(resp.text)['content']['isEULAAccepted']:	# only accept EULA if it is not already accepted
        url = '/api/instances/system/0/action/modify'
        args = {'isEulaAccepted':'true'}
        self._doPost(url, args)

  def updatePassword(self):
    self.updateUserPassword(self.username, self.password, self.newPassword)
    self.password = self.newPassword

  def updateUserPassword(self, username, password, newPassword):
    if password != newPassword:	# only update password if it is different from the existing one
      url = '/api/instances/user/user_' + username + '/action/modify'
      args = {'password':newPassword, 'oldPassword':password}
      self._doPost(url, args)

  def uploadLicense(self):
    isUpdate = False
    url = '/api/types/license/instances'
    params = {'fields': 'id, name, isInstalled, version, isValid, issued, expires, isPermanent'}
    resp = self._doGet(url, params)
    if resp.status_code // 100 == 2:
      if 'entries' in json.loads(resp.text):
        for entry in json.loads(resp.text)['entries']:
          if 'content' in entry:
            if 'isInstalled' in entry['content'] and entry['content']['isInstalled']:
              version = entry['content']['version']
            else:
              version = '0'
            isUpdate = self.isLicenseUpdate(self.licensePath, entry['content']['id'], version) or isUpdate 

    if isUpdate:
      url = self.apibase + '/upload/license'
      if self.checkMode:
        resp = None
      else:
        files = {'upload': open(self.licensePath, 'rb')}
        headers = {'X-EMC-REST-CLIENT':'true', 'EMC-CSRF-TOKEN': self.headers['EMC-CSRF-TOKEN']}
        resp = self.session.post(url, files = files, headers=headers, verify=False)
      self._postResult(resp, url, {'licensePath': self.licensePath})

  def isLicenseUpdate(self, licensePath, id, version='0'):
    r = re.compile('^INCREMENT ' + id + ' EMCLM ' + '(?P<new_version>\d+\.?\d*)')
    with open(licensePath, 'r') as f:
      for line in f:
        m = r.search(line)
        if m:
          if m.group('new_version') > version:
            self.updateResults.append({id + '_license_update': 'version ' + version + ' to version ' + m.group('new_version')})
            return True
    return False

  def processOtherUsers(self):
    for user in self.otherUsers:
      if user['username'] == 'admin':
        self.err = {'error': 'The module cannot update user "admin" through the "unity_other_users" parameter'}
        return
      if user['username'] in self.processedUsers:
        self.err = {'error': 'User "' + user['username'] +'" is defined more than once in the "unity_other_users" list'}
        return
      url = '/api/instances/user/user_' + user['username']
      params = {'fields':'id,name,role'}
      resp = self._doGet(url, params)
      if resp.status_code == 404:	# User not found
        self.err = None			# Suppress the error and create the user instead
        self.createUser(user)
      if self.err:
        return
      if resp.status_code != 404:	# User already exists in the system
        if 'password' in user:	# Verify existing user's password
          r = requests.get(self.apibase+'/api/instances/system/0', auth=requests.auth.HTTPBasicAuth(user['username'], user['password']), headers=self.headers, verify=False)
          self.processAuthResult(r, user['username'])
        if self.err:
          return
        if 'role' in user:	# Only update existing user's role
          self.updateUserRole(user['username'], json.loads(resp.text)['content']['role']['id'], user['role'])
        if self.err:
          return
      if 'new_password' in user:	# Update user's password. Newly created user's password can also be updated here.
        self.updateUserPassword(user['username'], user['password'], user['new_password'])
      if self.err:
        return
      self.processedUsers.append(user['username'])

  def updateUserRole(self, username, role, newRole):
    if role != newRole:
      url = '/api/instances/user/user_' + username + '/action/modify'
      args = {'role': newRole}
      self._doPost(url, args)

  def createUser(self, user):
    url = '/api/types/user/instances'
    role = 'administrator'	# default role
    if 'role' in user:
      role = user['role']
    args = {'name': user['username'], 'role': role, 'password': user['password']}
    self._doPost(url, args)
    
  def updateDnsServers(self):
    url = '/api/instances/dnsServer/0'
    params = {'fields':'addresses,domain,origin'}
    resp = self._doGet(url, params)
    if resp.status_code == 200:
      if json.loads(resp.text)['content']['addresses'] != self.dnsServers: 	# only update DNS servers if they are different from the current ones
        url = '/api/instances/dnsServer/0/action/modify'
        args = {'addresses': self.dnsServers}
        self._doPost(url, args)

  def updateNtpServers(self):
    url = '/api/instances/ntpServer/0'
    params = {'fields':'addresses'}
    resp = self._doGet(url, params)
    if resp.status_code == 200:
      if json.loads(resp.text)['content']['addresses'] != self.ntpServers: 	# only update NTP servers if they are different from the currently ones
        url = '/api/instances/ntpServer/0/action/modify'
        args = {'addresses': self.ntpServers, 'rebootPrivilege': self.ntpRebootPrivilege}
        return self._doPost(url, args)

  def runQueries(self):
    for query in self.queries:
      if not 'resource_type' in query:	# A query must have the "resource_type" parameter
        self.err = {'error': 'Query has no "resource_type" parameter', 'query': query}
        return
      instanceKeys = ['compact', 'fields', 'language']	# Instance query keys
      collectionKeys = ['compact', 'fields', 'filter', 'groupby', 'language', 'orderby', 'page', 'per_page', 'with_entrycount']	# Collection query keys
      if 'id' in query:
        url = '/api/instances/' + query['resource_type'] + '/' + query['id']
        paramKeys = instanceKeys
      else:
        url = '/api/types/' + query['resource_type'] + '/instances'
        paramKeys = collectionKeys
      params = {key: query[key] for key in paramKeys if key in query}	# dictioanry comprehension to create a sub-dictioanry from the query with only keys in paramKeys
      if 'compact' not in params:
        params['compact'] = 'true'	# By default, omit metadata from each instance in the query response
      if 'id' not in query and 'with_entrycount' not in params:	# Collection query without the 'with_entrycount' parameter
        params['with_entrycount'] = 'true'	# By default, return the entryCount response component in the response data.
      resp = self._doGet(url, params)
      if self.err:
        return
      else:
        r = json.loads(resp.text)
        result = {'resourceType': query['resource_type']}
        if 'id' in query:
          result['entries'] = [r]
          result['entryCount'] = 1
        else:
          result['entries'] = r['entries']
          if 'entryCount' in r:
            result['entryCount'] = r['entryCount']
        self.queryResults.append(result) 
  
  def run(self):
    self.startSession()
    if self.err:
      return
      
    if self.acceptEula:
      self.acceptEULA()
      if self.err:
        return
      
    if self.newPassword:
      self.updatePassword()
      if self.err:
        return

    if self.licensePath:
      self.uploadLicense()
      if self.err:
        return

    if self.otherUsers:
      self.processOtherUsers()
      if self.err:
        return

    if self.dnsServers:
      self.updateDnsServers()
      if self.err:
        return

    if self.ntpServers:
      self.updateNtpServers()
      if self.err:
        return

    if self.queries:
      self.runQueries()
      if self.err:
        return

    self.stopSession()

def main():
    module = AnsibleModule(
        argument_spec=dict(
            unity_hostname=dict(default=None, required=True, type='str'),
            unity_username=dict(default='admin', type='str'),
            unity_password=dict(default='Password123#', type='str', no_log=True),
            unity_accept_eula=dict(default=False, type='bool'),
            unity_new_password = dict(default=None, type='str', no_log=True),
            unity_license_path = dict(default=None, type='path'),
            unity_other_users = dict(default=None, type='list'),
            unity_dns_servers = dict(default=None, type='list'),
            unity_ntp_servers = dict(default=None, type='list'),
            unity_ntp_reboot_privilege = dict(default=0, type='int', choices=[0,1,2]),
            unity_queries = dict(default=None, type='list')
        ),
        supports_check_mode=True
    )

    unity = Unity(module)
    unity.run()
    if unity.err:
      module.fail_json(changed=unity.changed, msg = unity.err, unity_update_results = unity.updateResults, unity_query_results = unity.queryResults)
    else:
      module.exit_json(changed=unity.changed, unity_update_results = unity.updateResults, unity_query_results = unity.queryResults)

if __name__ == '__main__':
    main()

