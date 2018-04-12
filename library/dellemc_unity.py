#!/usr/bin/python

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: dellemc_unity
short_description: Configure and manage Dell EMC Unity Storage System
description:
    - This module can be used to configure and manage Dell EMC Unity Storage System.
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
    unity_updates:
        description: 
            - Update resources of the Unity system.
            - See "Unisphere Management REST API Programer's Guide" for examples of how to update Unity system resources.
            - See "Unisphere Management REST API Reference Guide" for details and arguments of each individual resource's update operations.
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
                    - ID of an instance of the resouce type to be updated.
                    - If this option is present, then instance update of the resouce type will be executed.
                    - Otherwise, if this option is missing, then the update operation either creates a new instance, or executes a class-level action.
                    - If the "action" option is present, then a class-level action on the resource type is executed.
                    - Otherwise, if the "action" option is missing, then a new instance of the resource type is created.
                required: false
                type: string
            action:
                description:
                    - Action of the update operation.
                    - If the "id" option is present, then the action is executed on the instance.
                    - Otherwise, if the "id" option is missing, then the action is executed at the class-level on the resouce type. 
                required: false
                default: "modify"
                type: string
            attributes:
                description:
                    - The attributes to compare to decide whether an update should be executed.
                    - If attributes are missing, then the default, hard-coded attribute will be compared against the existing values.
                    - If attributes is a list, then queries of attributes of the same names will be compared to the ones in the update.
                    - Sometimes an attribute in the query field is different from that as an update argument, in this case, a dictionary mapping queried attributes to update arguments can be used.
                    - If the update is on an instance with ID, then the attributes specifies which one of the current values of the instance should be compared with the values to be updated. If all values are the same, then the update will not be executed, but a warning will be issued.
                    - If the update is to create a new instance, then the attributes are used to search for instances of the same attribute values. If such duplicates exist, a warning will be issued in check mode.
                    - Dotted attributes can be used to compare related resources.
                required: false
                type: list or dictionary
            filter:
                description:
                    - A filter for query to find duplicates of an instance creation update.
                    - See "Unisphere Management REST API Programmer's Guide" for details on how to create a filter for queries.
                    - It can be a partial filter, complemented by the list of attributes to compare.
                    - If the filter is missing, then the default, hard-coded filter will be used.
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
            timeout:
                description:
                    - Seconds before timeout.
                    - Executes the request in the background. Most active management requests (ones that attempt to change the configuration) support this option. 
                    - The documentation for each API method in the Unisphere Management REST API Reference Guide specifies whether the method supports this option.
                required: false
                type: int
    unity_password_updates:
        description: 
            - Update passwords of users of the Unity system. a
        required: false
        type: list
        suboptions:
            username: 
                description:
                    - Name of the user.
                required: true
                type: string
            password:
                description:
                    - Current password of the user.
                required: true
                type: string
            new_password:
                description:
                    - New passowrd of the user.
                required: true
                type: string
    unity_queries:
        description:
            - Query the Unity system for resource information.
            - See "Unisphere Management REST API Programmer's Guide" for detailed description and examples of the query parameters.
            - See "Unisphere Management REST API Reference Guide" for details and attributes (field names) of each individual resource's query operations.
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
      - {resource_type: system, id: '0', attributes: {'isEULAAccepted':'isEulaAccepted'}, isEulaAccepted: 'true'}
    unity_password_updates:
      - {username: admin, password: Password123#, new_password: Password123!}
    unity_license_path: /home/labadmin/unity.lic

- name: Updates and queries
  dellemc_unity:
    unity_hostname: "192.168.0.202"
    unity_username: admin
    unity_password: Password123!
    unity_updates:
      - {resource_type: user, name: test1, password: Welcome1!, role: administrator, attributes: [name]}
      - {resource_type: user, id: 'user_test1', attributes: {'role.id':'role'}, role: 'operator'}
      - {resource_type: remoteSyslog, id: '0', enabled: True, address: '192.168.0.11:515', protocol: 1, facility: 0}
      - {resource_type: dnsServer, id: '0', addresses: [10.254.66.23, 10.254.66.24]}
      - {resource_type: ntpServer, id: '0', attributes: [addresses], addresses: [10.254.140.21, 10.254.140.22], rebootPrivilege: 2}
    unity_password_updates:
      - {username: test1, password: Welcome1!, new_password: Welcome2!}
    unity_queries:
      - {resource_type: user, id: 'user_test1', fields: 'role.id'}
      - {resource_type: remoteSyslog, id: "0", fields: 'address,protocol,facility,enabled'}      # id parameter has to be of the string type
      - {resource_type: dnsServer, fields: "domain, addresses, origin", page: 1, per_page: 100}
      - {resource_type: ntpServer, id: "0", fields: addresses}      # id parameter has to be of the string type

- name: Deletes
  dellemc_unity:
    unity_hostname: "192.168.0.202"
    unity_username: admin
    unity_password: Password123!
    unity_updates:
      - {resource_type: user, id: 'user_test1', action: 'delete'}
'''

RETURN = '''
unity_query_results:
    description:
        - A list of JSON objects detailing the results of each successful query operation.
    returned: always
    type: list
    sample: >
        "unity_query_results": [
            {
                "entries": [
                    {
                        "content": {
                            "id": "user_test1", 
                            "role": {
                                "id": "operator"
                            }
                        }
                    }
                ], 
                "entryCount": 1, 
                "query": {
                    "fields": "role.id", 
                    "id": "user_test1", 
                    "resource_type": "user"
                }, 
                "url": "https://192.168.0.202/api/instances/user/user_test1?compact=true&fields=role.id"
            }, 
            {
                "entries": [
                    {
                        "content": {
                            "address": "192.168.0.11:515", 
                            "enabled": true, 
                            "facility": 0, 
                            "id": "0", 
                            "protocol": 1
                        }
                    }
                ], 
                "entryCount": 1, 
                "query": {
                    "fields": "address,protocol,facility,enabled", 
                    "id": "0", 
                    "resource_type": "remoteSyslog"
                }, 
                "url": "https://192.168.0.202/api/instances/remoteSyslog/0?compact=true&fields=address%2Cprotocol%2Cfacility%2Cenabled"
            }, 
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
                "query": {
                    "fields": "domain, addresses, origin", 
                    "page": 1, 
                    "per_page": 100, 
                    "resource_type": "dnsServer"
                }, 
                "url": "https://192.168.0.202/api/types/dnsServer/instances?compact=true&fields=domain%2C+addresses%2C+origin&with_entrycount=true&page=1&per_page=100"
            }, 
            {
                "entries": [
                    {
                        "content": {
                            "addresses": [
                                "10.254.140.21", 
                                "10.254.140.22"
                            ], 
                            "id": "0"
                        }
                    }
                ], 
                "entryCount": 1, 
                "query": {
                    "fields": "addresses", 
                    "id": "0", 
                    "resource_type": "ntpServer"
                }, 
                "url": "https://192.168.0.202/api/instances/ntpServer/0?compact=true&fields=addresses"
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
        query:
            description:
                - The original query.
            returned: always
            type: complex
        url:
            description:
                - URL of the query.
            returned: always
            type: string

unity_update_results:
    description:
        - A list of JSON objects detailing the results of each operation.
    returned: always
    type: list
    sample: >
        "unity_update_results": [
            {
                "args": {
                    "name": "test1", 
                    "password": "Welcome1!", 
                    "role": "administrator"
                }, 
                "HTTP_method": "POST",
                "response": {
                    "@base": "https://192.168.0.202/api/instances/user", 
                    "content": {
                        "id": "user_test1"
                    }, 
                    "links": [
                        {
                            "href": "/user_test1", 
                            "rel": "self"
                        }
                    ], 
                    "updated": "2017-04-04T13:32:05.837Z"
                },
                "url": "https://192.168.0.202/api/types/user/instances"
            }, 
            {
                "args": {
                    "address": "192.168.0.11:515", 
                    "enabled": true, 
                    "facility": 0, 
                    "protocol": 1
                }, 
                "HTTP_method": "POST",
                "url": "https://192.168.0.202/api/instances/remoteSyslog/0/action/modify"
            }, 
            {
                "update": {
                    "addresses": [
                        "10.254.66.23", 
                        "10.254.66.24"
                    ], 
                    "id": "0", 
                    "resource_type": "dnsServer"
                }, 
                "warning": "The existing instances already has the same attributes as the update operation. No update will happen."
            }, 
            {
                "args": {
                    "addresses": [
                        "10.254.140.21", 
                        "10.254.140.22"
                    ], 
                    "rebootPrivilege": 2
                }, 
                "HTTP_method": "POST",
                "url": "https://192.168.0.202/api/instances/ntpServer/0/action/modify"
            },
            {
                "HTTP_method": "DELETE", 
                "url": "https://192.168.0.202/api/instances/user/user_test1"
            }
        ]
    contains:
        HTTP_method:
            description:
                - HTTP method used to effect the update.
            returned: success
            type: string
        url:
            description:
                - URL of the operation to change the resource.
            returned: success
            type: string
        args:
            description:
                - Arguments of the operation to change the resource.
            returned: success
            type: complex
        response:
            description:
                - Non-empty response of the update operation from the Unity system.
            returned: success
            type: complex
        update:
            description:
                - The original update request.
                - Only returned when the update failed.
            returned: failure
            type: complex
        message:
            description:
                - Warning or failure message of the failed update operation.
            returned: failure
            type: string

'''

#!/usr/bin/python

from ansible.module_utils.dellemc_unity import common_functions
import requests, json, re
from ansible.module_utils.basic import AnsibleModule
from datetime import datetime

actionAttribs = {
    'create': {
        'alertConfigSNMPTarget': {'address': 'targetAddress'},
        'capabilityProfile': ['name', 'pool'],
        'cifsServer': ['nasServer'],
        'pool': ['name'],
        'user': ['name']
    },
    'modify': {
        'alertConfig': {
            'locale': 'alertLocale',
            'isThresholdAlertsEnabled': 'isThresholdAlertsEnabled',
            'minEmailNotificationSeverity': 'minEmailNotificationSeverity',
            'minSNMPTrapNotificationSeverity': 'minSNMPTrapNotificationSeverity',
            'emailFromAddress': 'emailFromAddress',
            'destinationEmails': 'destinationEmails'
        },
        'alertConfigSNMPTarget': {
            'address': 'targetAddress',
            'username': 'username',
            'authProto': 'authProtocol',
            'privacyProto': 'privProtocol'
        },
        'capabilityProfile': ['name', 'description', 'usageTags'],
        'ntpServer': ['addresses'],
        'pool': {
            'name': 'name',
            'description': 'description',
            'storageResourceType': 'storageResourceType',
            'alertThreshold': 'alertThreshold',
            'poolSpaceHarvestHighThreshold': 'poolSpaceHarvestHighThreshold',
            'poolSpaceHarvestLowThreshold': 'poolSpaceHarvestLowThreshold',
            'snapSpaceHarvestHighThreshold': 'snapSpaceHarvestHighThreshold',
            'snapSpaceHarvestLowThreshold': 'snapSpaceHarvestLowThreshold',
            'isHarvestEnabled': 'isHarvestEnabled',
            'isSnapHarvestEnabled': 'isSnapHarvestEnabled',
            'isFASTCacheEnabled': 'isFASTCacheEnabled',
            'isFASTVpScheduleEnabled': 'isFASTVpScheduleEnabled',
            'poolFastVP.isScheduleEnabled': 'isFASTVpScheduleEnabled'
        },
        'system': {
            'name': 'name',
            'isUpgradeComplete': 'isUpgradeCompleted',
            'isAutoFailbackEnabled': 'isAutoFailbackEnabled',
            'isEULAAccepted': 'isEulaAccepted'
        },
        'cifsServer': ['name', 'description', 'netbiosName', 'domain', 'workgroup', 'nasServer'],
        'user': {'role.id': 'role'},
    },
}

actionFilters = {
    'create': {
    }
}


class Unity:

    def __init__(self, module):
        self.hostname = module.params['unity_hostname']
        self.username = module.params['unity_username']
        self.password = module.params['unity_password']

        self.licensePath = module.params['unity_license_path']
        self.updates = module.params['unity_updates']
        self.passwordUpdates = module.params['unity_password_updates']
        self.queries = module.params['unity_queries']

        self.poolCreator = module.params['create_pool']

        self.module = module
        self.checkMode = module.check_mode

        self.apibase = 'https://' + self.hostname  # Base URL of the REST API
        self.headers = {'X-EMC-REST-CLIENT': 'true', 'content-type': 'application/json',
                        'Accept': 'application/json'}  # HTTP headers for REST API requests, less the 'EMC-CSRF-TOKEN' header
        self.session = requests.Session()

        self.changed = False
        self.updateResults = []
        self.queryResults = []
        self.err = None

    def exitFail(self):
        self.module.fail_json(changed=self.changed, msg=self.err, unity_update_results=self.updateResults,
                              unity_query_results=self.queryResults)

    def exitSuccess(self):
        self.module.exit_json(changed=self.changed, unity_update_results=self.updateResults,
                              unity_query_results=self.queryResults)

    def _getMsg(self, resp):
        try:
            msg = json.loads(resp.text)
        except ValueError:
            msg = {'httpStatusCode': resp.status_code, 'messages': [{'en-US': resp.text}]}
        return msg

    def _getResult(self, resp, **kwargs):
        if resp.status_code // 100 == 2:  # HTTP status code 2xx = success
            return resp

        self.err = self._getMsg(resp)
        self.err.update({'url': resp.url})
        if resp.status_code == 401 and kwargs.get('auth'):  # Unauthorized password
            self.err['messages'][0]['en-US'] = "Authentication error for User '" + kwargs['auth'].username + "'"  # Update error message
        self.exitFail()

    def _doGet(self, url, params=None, **kwargs):
        if kwargs is None:
            kwargs = {}
        kwargs.update({'headers': self.headers, 'verify': False})
        resp = self.session.get(self.apibase + url, params=params, **kwargs)
        return self._getResult(resp, **kwargs)

    def _changeResult(self, resp, url, args=None, changed=True, msg=None, **kwargs):
        if resp:
            url = resp.url
        elif 'params' in kwargs:  # Reconstruct URL with parameters
            url += '?'
            for key, value in kwargs['params'].items():
                url += key + '=' + value + '&'
            url = url.strip('?&')
        if (resp is None) or (resp and resp.status_code // 100 == 2):
            if changed:
                self.changed = changed
            if changed or msg:
                changeContent = {'changed': changed}
                if args:
                    changeContent['args'] = args
                if resp and resp.text:  # append response if it exists
                    changeContent['response'] = json.loads(resp.text)
                if msg:  # append messages if they exist
                    changeContent.update(msg)
                self.updateResults.append(changeContent)
        else:
            self.err = self._getMsg(resp)
            self.err['url'] = resp.url
            if args is not None:
                self.err['args'] = args
            self.exitFail()

    def _doPost(self, url, args, changed=True, msg=None, **kwargs):
        if self.checkMode:
            resp = None
        else:
            if kwargs is None:
                kwargs = {}
            kwargs.update({'headers': self.headers, 'verify': False})
            resp = self.session.post(self.apibase + url, json=args, **kwargs)
        self._changeResult(resp, url, args, changed=changed, msg=msg, **kwargs)

    def _doDelete(self, url, msg=None, **kwargs):
        if self.checkMode:
            resp = None
        else:
            if kwargs is None:
                kwargs = {}
            kwargs.update({'headers': self.headers, 'verify': False})
            resp = self.session.delete(self.apibase + url, **kwargs)
        self._changeResult(resp, url, msg=msg, **kwargs)

    def startSession(self):
        url = '/api/instances/system/0'
        auth = requests.auth.HTTPBasicAuth(self.username, self.password)
        resp = self._doGet(url, auth=auth)
        # Add 'EMC-CSRF-TOKEN' header
        self.headers['EMC-CSRF-TOKEN'] = resp.headers['EMC-CSRF-TOKEN']

    def stopSession(self):
        url = '/api/types/loginSessionInfo/action/logout'
        args = {'localCleanupOnly': 'true'}
        self._doPost(url, args, changed=False)

    def uploadLicense(self):
        url = self.apibase + '/upload/license'
        resp = None
        msg = {'resource_type': 'license', 'action': 'upload'}
        changed = self.isLicenseUpdate()
        if changed:
            if not self.checkMode:
                files = {'upload': open(self.licensePath, 'rb')}
                headers = {'X-EMC-REST-CLIENT': 'true', 'EMC-CSRF-TOKEN': self.headers['EMC-CSRF-TOKEN']}
                resp = self.session.post(url, files=files, headers=headers, verify=False)
        else:
            msg.update({'warn': 'All licenses are up-to-date. No upload will happen.'})
        self._changeResult(resp, url, args={'licensePath': self.licensePath}, changed=changed, msg=msg)

    def isLicenseUpdate(self):
        isUpdate = False
        query = {'resource_type': 'license', 'fields': 'id, name, issued'}
        result = self.runQuery(query)
        oldIssued = {}
        for entry in result['entries']:
            if entry.get('id'):
                oldIssued[entry['id'].upper()] = datetime.strptime(entry.get('issued', '1970-01-01T00:00:00.000Z'),
                                                                   '%Y-%m-%dT%H:%M:%S.%fZ')

        reID = re.compile('^INCREMENT (?P<id>\w+)')
        reIssued = re.compile('ISSUED=(?P<issued>\d{1,2}-[A-Z][a-z]{2}-\d{4})')
        newIssued = {}
        id = None
        with open(self.licensePath, 'r') as f:
            for line in f:
                if id is None:
                    m = reID.search(line)
                    if m:
                        id = m.group('id').upper()
                else:
                    m = reIssued.search(line)
                    if m:
                        newIssued[id] = datetime.strptime(m.group('issued'), '%d-%b-%Y')
                        id = None

        for id in newIssued.keys():
            if newIssued[id] > oldIssued.get(id, datetime(1970, 1, 1)):
                isUpdate = True
        return isUpdate

    def runUpdates(self):
        for update in self.updates:
            self.runUpdate(update)

    def runUpdate(self, update):
        paramKeys = ['language', 'timeout']
        urlKeys = ['resource_type', 'id', 'action', 'attributes', 'filter'] + paramKeys
        params = {key: update[key] for key in update if key in paramKeys}
        args = {key: update[key] for key in update if key not in urlKeys}
        msg = {}

        if 'resource_type' in update:  # A resource must have the "resource_type" parameter
            msg['resource_type'] = update['resource_type']
        else:
            self.err = {'error': 'Update has no "resource_type" parameter', 'update': update}
            self.exitFail()

        if 'id' in update:  # Update an existing resource instance with ID
            msg['id'] = update['id']
            url = '/api/instances/' + update['resource_type'] + '/' + update['id'] + '/action/' + update.get('action',
                                                                                                             'modify')
            if 'action' not in update:
                update['action'] = 'modify'  # default action
                msg['action'] = update['action']
                if self.isDuplicate(update):
                    msg['warn'] = 'The existing instances already has the same attributes as the update operation. ' \
                                  'No update will happen.'
                    self._changeResult(None, url, args, changed=False, msg=msg, params=params)
                    return
            elif update['action'] == 'delete':
                msg = update
                url = '/api/instances/' + update['resource_type'] + '/' + update['id']
                if not self.isDuplicate(update):
                    msg['warn'] = 'The instance to be deleted does not exist. No update will happen.'
                    self._changeResult(None, url, args, changed=False, msg=msg, params=params)
                    return
                else:
                    resp = self._doDelete(url, msg)
                    return
        else:
            if 'action' in update:  # Class-level action
                url = '/api/types/' + update['resource_type'] + '/action/' + update['action']
            else:
                update['action'] = 'create'  # Create a new instance
                msg['action'] = update['action']
                url = '/api/types/' + update['resource_type'] + '/instances'
                if self.checkMode:  # Only check duplicate entries during check mode. The users accept the consequences if they still want to add the new instance
                    duplicates = self.isDuplicate(update)
                    if duplicates:
                        msg.update({
                            'warn': 'Instances with the same attributes already exist for the creation operation. Create the new instance at your own risk.',
                            'duplicates': duplicates})
                        self._changeResult(None, url, args, changed=False, msg=msg, params=params)
                        return
        msg['action'] = update['action']
        resp = self._doPost(url, args, params=params, msg=msg)
        return resp

    def getModelOfUnity(self):
        resp = self.runQuery({'resource_type': 'system', "fields": 'model'})
        model = resp['entries'][0]['model']  # get model of Unity from JSON response
        return model

    def createPool(self):
        params = self.poolCreator
        updateRequest = {'resource_type': 'pool'}
        model = self.getModelOfUnity()

        if model == 'UnityVSA':
            requiredParameters = {'name', 'pool_unit_params'}
            optionalParameters = {'type', 'isFASTVpSheduleEnabled', 'description'}
            if not common_functions.checkParameters(params, requiredParameters, optionalParameters):
                self.module.fail_json(changed=False, msg="Error in function create_pool",
                                      exception="You haven't inputted all required parameters or have inputted"
                                                " unsupported optional0 parameter(s)",
                                      required_parametrs_for_command=requiredParameters,
                                      optional_parametrs=optionalParameters)

            name = params['name']
            poolUnitParameters = params['pool_unit_params']
            updateRequest.update({'name': name})
            updateRequest.update({'addPoolUnitParameters': poolUnitParameters})

            for key in optionalParameters:
                if params.get(key):
                    updateRequest.update({key: params.get(key)})
            self.runUpdate(updateRequest)

        else:
            self.module.fail_json(changed=False, exception="I don't work with such Unity yet", unity_model=model)

    def isDuplicate(self, update):
        # If this is an password update, then only proceed when the password is different from the old one
        if 'password' in update and 'oldPassword' in update:
            return update['password'] == update['oldPassword']

        # If this is an update of Proxy password, then do no checks because it is not possible to verify the HTTP Proxy's password
        if 'proxyPassword' in update:
            return False

        query = {key: update[key] for key in update if key in ['resource_type', 'id', 'language']}
        attrs = None
        filter = None

        if update['action'] in ['create', 'modify']:  # Only create or modify actions
            # need to compare attributes with existing resource instances
            # First, use the default, hard-coded attributes
            attrs = actionAttribs[update['action']].get(update['resource_type'])

            # Next, if there is customer supplied attributes in the Ansible task, then override the default attributes
            if 'attributes' in update:
                attrs = update['attributes']

            # Last, if attributes is still not set, then use all attributes in the update that are resource-type specific
            if attrs is None:  # if attributes to catch duplicates are not specified, find them in the update parameters
                attrs = {attr: attr for attr in update if
                         attr not in ['resource_type', 'id', 'action', 'language', 'timeout', 'password',
                                      'new_password', 'attributes', 'filter']}

            if isinstance(attrs, list):
                attributes = {attr: attr for attr in attrs}
            elif isinstance(attrs, dict):
                attributes = attrs

        if update['action'] == 'create':  # Only create action needs a filter to find duplicates
            # First, use the default, hard-coded filter
            filter = actionFilters[update['action']].get(update['resource_type'])

            # Next, if there is customer supplied filter in the Ansible task, then override the default filter
            if 'filter' in update:
                filter = update['filter']

            # Last, if filter is still not set, then set it to empty string
            if filter is None:
                filter = ''

        if update['action'] == 'modify':  # Only modify action adds the 'fields' argument to the query
            query['fields'] = ','.join([field for field in attributes.keys() if attributes[field] in update])
        elif update['action'] == 'create':  # Only create action adds the 'filter' argument to the query
            for queryAttr, updateAttr in attributes.items():
                if updateAttr in update:
                    filter = queryAttr + self.processFilterValue(
                        self.getDottedValue(update, updateAttr)) + ' and ' + filter
            filter = re.sub(' and $', '', filter)  # strip the trailing 'and' if the original filter is empty string
            query['filter'] = filter

        result = self.runQuery(query)

        if update['action'] == 'modify':  # For modify action, compare queried attributes and update attributes
            content = result
            for queryAttr, updateAttr in attributes.items():
                if updateAttr in update and self.getDottedValue(content, queryAttr) != self.getDottedValue(update,
                                                                                                           updateAttr):
                    return False
            else:
                return True
        elif 'entries' in result and len(result['entries']) > 0:  # For class-level queries,
            #  the updated resource is a duplicate if the query returns some entries
            return result['entries']
        elif 'id' in result:  # For instance level queries, the updated resource is a duplicate if the query result contains the 'id' field
            return result
        else:
            return None

    def getDottedValue(self, dictionary, dottedKey, separator='.'):
        value = dictionary
        for key in dottedKey.split(separator):
            if value:
                value = value.get(key)
            else:
                break
        return value

    def processFilterValue(self, value):
        if isinstance(value, str):
            value = ' eq "' + value + '"'
        else:
            value = ' eq ' + str(value)
        return value

    def runPasswordUpdates(self):
        for update in self.passwordUpdates:
            self.runPasswordUpdate(update)

    def runPasswordUpdate(self, update):
        username = update.get('username')
        password = update.get('password')
        newPassword = update.get('new_password')
        kwargs = {'auth': requests.auth.HTTPBasicAuth(username, password), 'headers': self.headers, 'verify': False}
        resp = requests.get(self.apibase + '/api/instances/system/0', **kwargs)
        self._getResult(resp, **kwargs)  # process get results
        update = {'resource_type': 'user', 'id': 'user_' + username, 'password': newPassword, 'oldPassword': password}
        self.runUpdate(update)

    def runQueries(self):
        for query in self.queries:
            result = self.runQuery(query)
            self.queryResults.append(result)

    def runQuery(self, query):
        if not 'resource_type' in query:  # A query must have the "resource_type" parameter
            self.err = {'error': 'Query has no "resource_type" parameter', 'query': query}
            self.exitFail()
        instanceKeys = ['compact', 'fields', 'language']  # Instance query keys
        collectionKeys = ['compact', 'fields', 'filter', 'groupby', 'language', 'orderby', 'page', 'per_page',
                          'with_entrycount']  # Collection query keys
        if 'id' in query:
            url = '/api/instances/' + query['resource_type'] + '/' + query['id']
            paramKeys = instanceKeys
        else:
            url = '/api/types/' + query['resource_type'] + '/instances'
            paramKeys = collectionKeys
        params = {key: query[key] for key in paramKeys if
                  key in query}  # dictioanry comprehension to create a sub-dictioanry from the query with only keys in paramKeys
        if 'compact' not in params:
            params['compact'] = 'true'  # By default, omit metadata from each instance in the query response
        if 'id' not in query and 'with_entrycount' not in params:  # Collection query without the 'with_entrycount' parameter
            params['with_entrycount'] = 'true'  # By default, return the entryCount response component in the response data.
        resp = self._doGet(url, params)
        r = json.loads(resp.text)
        result = {'resource_type': query['resource_type']}
        if 'id' in query:
            result['id'] = query['id']
            result.update(r['content'])
        else:
            result['entries'] = []
            for entry in r['entries']:
                result['entries'].append(entry['content'])
        return result

    def run(self):
        self.startSession()
        if self.updates:
            self.runUpdates()

        if self.poolCreator:
            self.createPool()

        if self.passwordUpdates:
            self.runPasswordUpdates()

        if self.licensePath:
            self.uploadLicense()

        if self.queries:
            self.runQueries()

        self.stopSession()


def main():
    argument_spec = dict(
        unity_hostname=dict(default=None, required=True, type='str'),
        unity_username=dict(default='admin', type='str'),
        unity_password=dict(default='Password123#', type='str'),  # , no_log=True),
        unity_queries=dict(default=None, type='list'),
        unity_updates=dict(default=None, type='list'),

        unity_license_path=dict(default=None, type='path'),
        unity_password_updates=dict(default=None, type='list'),  # , no_log=True),
        create_pool=dict(default=None, required=False, type='dict')

    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    unity = Unity(module)
    unity.run()
    if unity.err:
        unity.exitFail()
    else:
        unity.exitSuccess()


if __name__ == '__main__':
    main()
