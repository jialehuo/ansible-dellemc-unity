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
'''

RETURN = '''
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

    self.checkMode = module.check_mode

    self.processedUsers = []
    self.apibase = 'https://' + self.hostname	# Base URL of the REST API
    self.headers = {'X-EMC-REST-CLIENT': 'true', 'content-type': 'application/json', 'Accept': 'application/json'}       # HTTP headers for REST API requests, less the 'EMC-CSRF-TOKEN' header
    self.session = requests.Session()
    self.changed = False
    self.msg = []
    self.err = None

  def _getMsg(self, resp):
    return {'status_code': resp.status_code, 'text': resp.text}

  def _getResult(self, resp):
    if resp.status_code // 100 == 2:	# HTTP status code 2xx = success
      pass
      # self.msg.append(self._getMsg(resp)) 
    else:
      self.err = self._getMsg(resp)
    return resp

  def _postResult(self, resp, url, args, changed=True):
    changedTxt = 'Changed'
    if self.checkMode:
      changedTxt = 'To be changed'

    if self.checkMode or (resp and resp.status_code // 100 == 2):
      if changed:
        self.changed = changed
        self.msg.append({changedTxt: {'url': url, 'args': args}})
    else:
      self.err = self._getMsg(resp)
      self.err.update({'url': url, 'args': args})

  def _doPost(self, url, args, changed=True):
    if self.checkMode:
      resp = None
    else:
      resp = self.session.post(self.apibase + url, json = args, headers=self.headers, verify=False)
    self._postResult(resp, url, args, changed)

  def _doGet(self, url, params):
    return self._getResult(self.session.get(self.apibase + url, params=params, headers=self.headers, verify=False))

  def processAuthResult(self, resp, username):
    self._getResult(resp)
    if self.err: 	
      if resp.status_code == 401:	# Unauthorized password
        self.err['text'] = 'User "' + username + '" is not authenticated because of wrong password'	# Update error message
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
            self.msg.append({'License update for ' + id: 'version ' + version + ' to version ' + m.group('new_version')})
            return True
    return False

  def processOtherUsers(self):
    for user in self.otherUsers:
      if user['username'] == 'admin':
        self.err = {'failure': 'The module cannot update user "admin" through the "unity_other_users" parameter'}
        return
      if user['username'] in self.processedUsers:
        self.err = {'failure': 'User "' + user['username'] +'" is defined more than once in the "unity_other_users" list'}
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
  
  def update(self):
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
            unity_ntp_reboot_privilege = dict(default=0, type='int')
        ),
        supports_check_mode=True
    )

    unity = Unity(module)
    unity.update()
    if unity.err:
      unity.msg.append(unity.err)
      module.exit_json(changed=unity.changed, failed=True, msg = unity.msg)
    else:
      module.exit_json(changed=unity.changed, msg=unity.msg)

if __name__ == '__main__':
    main()

