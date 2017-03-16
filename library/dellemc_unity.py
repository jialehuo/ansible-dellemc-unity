#!/usr/bin/python

import requests, json
from ansible.module_utils.basic import AnsibleModule

class Unity:

  def __init__(self, module):
    self.hostname = module.params['unity_hostname']
    self.username = module.params['unity_username']
    self.password = module.params['unity_password']
    self.acceptEula = module.params['unity_accept_eula']
    self.newPassword = module.params['unity_new_password']
    self.licensePath = module.params['unity_license_path']
    self.dnsServers = module.params['unity_dns_servers']
    self.ntpServers = module.params['unity_ntp_servers']

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
      self.msg.append(self._getMsg(resp)) 
    else:
      self.err = self._getMsg(resp)
    return resp

  def _postResult(self, resp, url, args):
    if resp.status_code // 100 == 2:
      self.changed = True
      self.msg.append({'Updated': {'url': url, 'args': str(args)}})
    else:
      self.err = self._getMsg(resp)
      self.err.update({'url': url, 'args': str(args)})

  def _doPost(self, url, args):
    resp = self.session.post(self.apibase + url, json = args, headers=self.headers, verify=False)
    self._postResult(resp, url, args)

  def _doGet(self, url, params):
    return self._getResult(self.session.get(self.apibase + url, params=params, headers=self.headers, verify=False))

  def startSession(self):
    resp = self.session.get(self.apibase+'/api/instances/system/0', auth=requests.auth.HTTPBasicAuth(self.username, self.password), headers=self.headers, verify=False)
    self._getResult(resp)
    if resp.status_code // 100 == 2:	# 2xx status code - success
      # Add 'EMC-CSRF-TOKEN' header
      self.headers['EMC-CSRF-TOKEN']=resp.headers['EMC-CSRF-TOKEN']

  def stopSession(self):
    url = '/api/types/loginSessionInfo/action/logout'
    args = {'localCleanupOnly' : 'true'}
    self._doPost(url, args)

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
    if self.password != self.newPassword:	# only update password if it is different from the existing one
      url = '/api/instances/user/user_' + self.username + '/action/modify'
      args = {'password':self.newPassword, 'oldPassword':self.password}
      self._doPost(url, args)
      self.password = self.newPassword

  def uploadLicense(self):
    url = self.apibase + '/upload/license'
    files = {'upload': open(self.licensePath, 'rb')}
    headers = {'X-EMC-REST-CLIENT':'true', 'EMC-CSRF-TOKEN': self.headers['EMC-CSRF-TOKEN']}
    resp = self.session.post(url, files = files, headers=headers, verify=False)
    self._postResult(resp, url, {'licensePath': self.licensePath})

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
        args = {'addresses': self.ntpServers, 'rebootPrivilege': 2}
        return self._doPost(url, args)
  
  def update(self):
    self.startSession()
    if self.err != None:
      return
      
    if self.acceptEula:
      self.acceptEULA()
      if self.err != None:
        return
      
    if self.newPassword:
      self.updatePassword()
      if self.err != None:
        return

    if self.licensePath:
      self.uploadLicense()
      if self.err != None:
        return

    if self.dnsServers:
      self.updateDnsServers()
      if self.err != None:
        return

    if self.ntpServers:
      self.updateNtpServers()
      if self.err != None:
        return

    self.stopSession()

def main():
    module = AnsibleModule(
        argument_spec=dict(
            unity_hostname=dict(default=None, required=True, type='str'),
            unity_username=dict(default=None, required=True, type='str'),
            unity_password=dict(default=None, required=True, type='str', no_log=True),
            unity_accept_eula=dict(default=None, type='bool'),
            unity_new_password = dict(default=None, type='str', no_log=True),
            unity_license_path = dict(default=None, type='path'),
            unity_dns_servers = dict(default=None, type='list'),
            unity_ntp_servers = dict(default=None, type='list')
        )
    )

    unity = Unity(module)
    unity.update()
    if unity.err != None:
      unity.msg.append(unity.err)
      module.exit_json(changed=unity.changed, failed=True, msg = unity.msg)
    else:
      module.exit_json(changed=unity.changed, msg=unity.msg)

if __name__ == '__main__':
    main()

