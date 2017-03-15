#!/usr/bin/python

import requests, json
from ansible.module_utils.basic import AnsibleModule

class UnitySession:

  def __init__(self, host, username, password):
    self.host = host
    self.username = username 
    self.password = password
    self.base = "https://" + host + "/api"      # Base URL of the REST API
    self.session = requests.Session()
    self.headers = {'X-EMC-REST-CLIENT': 'true', 'content-type': 'application/json', 'Accept': 'application/json'}       # HTTP headers for REST API requests, less the 'EMC-CSRF-TOKEN' header

  def doPost(self, url, args):
    r = self.session.post(url, json = args, headers=self.headers, verify=False)
    return r.status_code, r.text

  def doGet(self, url, params):
    r = self.session.get(url, params=params, headers=self.headers, verify=False)
    return r.status_code, r.text

  def start(self):
    r = self.session.get(self.base+"/instances/system/0", auth=requests.auth.HTTPBasicAuth(self.username, self.password), headers=self.headers, verify=False)
    if r.status_code == 200:
      # Add 'EMC-CSRF-TOKEN' header
      self.headers['EMC-CSRF-TOKEN']=r.headers['EMC-CSRF-TOKEN']
      return True	# Session started
    else:
      return False	# Session not started

  def stop(self):
    url = self.base + '/types/loginSessionInfo/action/logout'
    args = {"localCleanupOnly" : "true"}
    return self.doPost(url, args)

  def acceptEULA(self):
    url = self.base+"/instances/system/0/action/modify"
    args = {'isEulaAccepted':'true'}
    return self.doPost(url, args)

  def updatePassword(self, newPassword):
    url = self.base+'/instances/user/user_' + self.username + '/action/modify'
    args = {'password':newPassword, 'oldPassword':self.password}
    self.password = newPassword
    return self.doPost(url, args)

  def uploadLicense(self, licensePath):
    url = "https://" + self.host + '/upload/license'
    files = {'upload': open(licensePath, 'rb')}
    headers = {'X-EMC-REST-CLIENT':'true', 'EMC-CSRF-TOKEN': self.headers['EMC-CSRF-TOKEN']}
    r = self.session.post(url, files = files, headers=headers, verify=False)
    return r.status_code, r.text

  def updateDnsServers(self, dnsServers):
    url = self.base + '/instances/dnsServer/0'
    params = {'fields':'addresses,domain,origin'}
    status_code, text = self.doGet(url, params)
    if status_code == 200:
      if json.loads(text)["content"]["addresses"] != dnsServers: 
        url = self.base + '/instances/dnsServer/0/action/modify'
        args = {'addresses': dnsServers}
        return self.doPost(url, args)
      else:
        return status_code, text

  def updateNtpServers(self, ntpServers):
    url = self.base + '/instances/ntpServer/0'
    params = {'fields':'addresses'}
    status_code, text = self.doGet(url, params)
    if status_code == 200:
      if json.loads(text)["content"]["addresses"] != ntpServers: 
        url = self.base + '/instances/ntpServer/0/action/modify'
        args = {'addresses': ntpServers, 'rebootPrivilege': 2}
        return self.doPost(url, args)
      else:
        return status_code, text

def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(default='sync', choices=['sync', 'manual'], type='str'),
            force=dict(default='no', type='bool'),
            date_time=dict(default=None, type='str'),
            unity_username=dict(default=None, required=True, type='str'),
            unity_password=dict(default=None, required=True, type='str',
                                no_log=True),
            unity_hostname=dict(default=None, required=True, type='str'),
        )
    )

    session = UnitySession(module.params["unity_hostname"], module.params["unity_username"], module.params["unity_password"])
    if session.start():
      resp = session.acceptEULA()
      session.stop()
      module.exit_json(changed=True, msg=resp)


if __name__ == '__main__':
    main()

