#!/usr/bin/python
import requests, json, re
from ansible.module_utils.basic import AnsibleModule
from datetime import datetime


ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}


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
        self.module = module
        self.hostname = module.params['unity_hostname']
        self.username = module.params['unity_username']
        self.password = module.params['unity_password']

        self.licensePath = module.params['unity_license_path']
        self.updates = module.params['unity_updates']
        self.passwordUpdates = module.params['unity_password_updates']
        self.queries = module.params['unity_queries']

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
            self.err['messages'][0]['en-US'] = "Authentication error for User '" + kwargs[
                'auth'].username + "'"  # Update error message
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
                    self._doDelete(url, msg)
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
            params[
                'with_entrycount'] = 'true'  # By default, return the entryCount response component in the response data.
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
        unity_license_path=dict(default=None, type='path'),
        unity_updates=dict(default=None, type='list'),
        unity_password_updates=dict(default=None, type='list'),  # , no_log=True),
        unity_queries=dict(default=None, type='list'),

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
