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
    unity_license_path:
        description:
            - Path to the license file of the Unity system.
        required: false
        type: string
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
    unity_updates:
      - {resource_type: system, id: '0', fields: {'isEULAAccepted':'isEulaAccepted'}, isEulaAccepted: 'true'}
    unity_update_passwords:
      - {username: admin, password: Password123#, new_password: Password123!}
    unity_license_path: /home/labadmin/unity.lic


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
                "change": {
                    "args": {
                        "isEulaAccepted": "true"
                    },
                    "url": "/api/instances/system/0/action/modify"
                }
            },
            {
                "change": {
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
                "change": {
                    "args": {
                        "licensePath": "/home/labadmin/unity.lic"
                    },
                    "url": "https://192.168.0.202/upload/license"
                }
            },
            {
                "change": {
                    "args": {
                        "name": "test1",
                        "password": "Welcome1!",
                        "role": "administrator"
                    },
                    "url": "/api/types/user/instances"
                }
            },
            {
                "change": {
                    "args": {
                        "name": "test2",
                        "password": "Welcome1!",
                        "role": "operator"
                    },
                    "url": "/api/types/user/instances"
                }
            },
            {
                "change": {
                    "args": {
                        "name": "test3",
                        "password": "Welcome1!",
                        "role": "administrator"
                    },
                    "url": "/api/types/user/instances"
                }
            },
            {
                "change": {
                    "args": {
                        "oldPassword": "Welcome1!",
                        "password": "Welcome1#"
                    },
                    "url": "/api/instances/user/user_test3/action/modify"
                }
            },
            {
                "change": {
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
                "change": {
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
        change:
            description:
                - Resource change in the Unity system.
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

'''

import requests, json, re
from ansible.module_utils.basic import AnsibleModule

class Unity:

  def __init__(self, module):
    self.hostname = module.params['unity_hostname']
    self.username = module.params['unity_username']
    self.password = module.params['unity_password']
    self.licensePath = module.params['unity_license_path']
    self.updates = module.params['unity_updates']
    self.passwordUpdates = module.params['unity_password_updates']
    self.queries = module.params['unity_queries']

    self.module = module
    self.checkMode = module.check_mode

    self.processedUsers = []
    self.apibase = 'https://' + self.hostname	# Base URL of the REST API
    self.headers = {'X-EMC-REST-CLIENT': 'true', 'content-type': 'application/json', 'Accept': 'application/json'}       # HTTP headers for REST API requests, less the 'EMC-CSRF-TOKEN' header
    self.session = requests.Session()
    self.changed = False
    self.updateResults = []
    self.queryResults = []
    self.err = None

  def exitFail(self):
      self.module.fail_json(changed=self.changed, msg = self.err, unity_update_results = self.updateResults, unity_query_results = self.queryResults)
   
  def exitSuccess(self):
    self.module.exit_json(changed=self.changed, unity_update_results = self.updateResults, unity_query_results = self.queryResults)

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
      self.exitFail()
    return resp
 
  def _postResult(self, resp, url, args, changed=True, **kwargs):
    changedTxt = 'change'
    if resp:
      url = resp.url
    elif 'params' in kwargs:	# Reconstruct URL with parameters
      url += '?'
      for key, value in kwargs['params'].items():
        url += key + '=' + value + '&'
      url = url.strip('?&')
    if self.checkMode or (resp and resp.status_code // 100 == 2):
      if changed:
        self.changed = changed
        changeContent =  {'url': url, 'args': args}
        if resp and resp.text:
          changeContent.update(json.loads(resp.text))
        self.updateResults.append({changedTxt: changeContent})
    else:
      self.err = self._getMsg(resp)
      self.err.update({'url': url, 'args': args})
      self.exitFail()

  def _doGet(self, url, params):
    return self._getResult(self.session.get(self.apibase + url, params=params, headers=self.headers, verify=False))

  def _doPost(self, url, args, changed=True, **kwargs):
    if self.checkMode:
      resp = None
    else:
      if kwargs is None:
        kwargs = {}
      kwargs.update({'headers': self.headers, 'verify': False})
      resp = self.session.post(self.apibase + url, json = args, **kwargs)
    self._postResult(resp, url, args, changed=changed, **kwargs)

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

  def runPasswordUpdates(self):
    for update in self.passwordUpdates:
      self.runPasswordUpdate(update)

  def runPasswordUpdate(self, update):
    username = update.get('username')
    password = update.get('password')
    newPassword = update.get('new_password')
    r = requests.get(self.apibase+'/api/instances/system/0', auth=requests.auth.HTTPBasicAuth(username, password), headers=self.headers, verify=False)
    self.processAuthResult(r, username)
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

  def runQueries(self):
    for query in self.queries:
      result = self.runQuery(query)
      self.queryResults.append(result)

  def runQuery(self, query):
      if not 'resource_type' in query:	# A query must have the "resource_type" parameter
        self.err = {'error': 'Query has no "resource_type" parameter', 'query': query}
        self.exitFail()
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
      r = json.loads(resp.text)
      result = {'resourceType': query['resource_type']}
      if 'id' in query:
        result['entries'] = [r]
        result['entryCount'] = 1
      else:
        result['entries'] = r['entries']
        result['entryCount'] = r.get('entryCount', len(r['entries']))
      return result

  def runUpdates(self):
    for update in self.updates:
      self.runUpdate(update)

  def runUpdate(self, update):
      if not 'resource_type' in update:	# A resource must have the "resource_type" parameter
        self.err = {'error': 'Update has no "resource_type" parameter', 'update': update}
        self.exitFail()

      if 'id' in update:	# Update an existing resource instance with ID
        if 'action' in update:
          action = update['action']
        else:
          action = 'modify' # default action
          if 'fields' in update:
            if self.isSameAsCurrent(update):	# Update values are the same as the current ones, so no need to do the update
              return
        url = '/api/instances/' + update['resource_type'] + '/' + update['id'] + '/action/' + action
      else:
        if 'action' in update:	# Class-level action
          url = '/api/types/' + update['resource_type'] + '/action/' + update['action']
        else:	# Create a new instance
          if self.checkMode:
            duplicates = self.isDuplicate(update)
            if duplicates:
              self.updateResults.append({'warning': 'Instances with similar parameters already exist for the creation operation', 'update': update, 'duplicates': duplicates})
              return
          url = '/api/types/' + update['resource_type'] + '/instances'
      paramKeys = ['language', 'timeout']
      urlKeys = ['resource_type', 'id', 'action', 'fields'] + paramKeys
      params = {key: update[key] for key in update if key in paramKeys}
      args = {key: update[key] for key in update if key not in urlKeys}
  
      resp = self._doPost(url, args, params = params)

  def isSameAsCurrent(self, update):
    query = {key: update[key] for key in update if key in ['resource_type', 'id', 'language']}
    fields = {}
    if 'fields' in update:
      if isinstance(update['fields'], str):
        fields = {field.strip(): field.strip() for field in update['fields'].split(',')}
      elif isinstance(update['fields'], dict):
        fields = update['fields']
      elif isinstance(update['fields'], list):
        fields = {field: field for field in update['fields']}
      
    query['fields'] = ','.join(fields.keys())
    queryResult = self.runQuery(query)
    content = queryResult['entries'][0]['content']
    for queryField, updateField in fields.items():
      queryValue = self.getDottedValue(content, queryField)
      updateValue = self.getDottedValue(update, updateField)
      if queryValue != updateValue:
        return False
    else:
      return True

  def isDuplicate(self, update):
    query = {key: update[key] for key in update if key in ['resource_type', 'language']}
    fields = None
    if 'fields' in update:
      if isinstance(update['fields'], list):
        fields = {field: field for field in update['fields']}
      elif isinstance(update['fields'], dict):
        fields = update['fields']
    if fields == None:
      fields = {field: field for field in update if field not in ['resource_type', 'id', 'action', 'fields', 'language', 'timeout', 'password', 'new_password']}
    filter = ''
    for queryField, updateField in fields.items():
      filter += queryField + ' eq ' + self.processFilterValue(self.getDottedValue(update, updateField)) + ' and '
    filter = re.sub(' and $', '', filter)
    query['filter'] = filter
    result = self.runQuery(query)
    if result['entryCount'] > 0: 
      return result['entries']
    else:
      return None

  def getDottedValue(self, dictionary, dottedKey, separator = '.'):
    value = dictionary
    for key in dottedKey.split(separator):
      if value:
        value = value.get(key)
      else:
        break
    return value

  def processFilterValue(self, value):
    if isinstance(value, str):
      value = '"' + value + '"'
    return value

  def run(self):
    self.startSession()

    if self.updates:
      self.runUpdates()

    if self.passwordUpdates:
      self.runPasswordUpdates()

    if self.licensePath:
      self.uploadLicense()

    if self.queries:
      self.runQueries()

    self.stopSession()

def main():
    module = AnsibleModule(
        argument_spec=dict(
            unity_hostname=dict(default=None, required=True, type='str'),
            unity_username=dict(default='admin', type='str'),
            unity_password=dict(default='Password123#', type='str', no_log=True),
            unity_license_path = dict(default=None, type='path'),
            unity_updates = dict(default=None, type='list'),
            unity_password_updates = dict(default=None, type='list'),
            unity_queries = dict(default=None, type='list')
        ),
        supports_check_mode=True
    )

    unity = Unity(module)
    unity.run()
    if unity.err:
      unity.exitFail()
    else:
      unity.exitSuccess()

if __name__ == '__main__':
    main()

