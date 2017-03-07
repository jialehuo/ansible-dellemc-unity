import requests, json

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

  def startSession(self):
    r = self.session.get(self.base+"/instances/system/0", auth=requests.auth.HTTPBasicAuth(self.username, self.password), headers=self.headers, verify=False)
    if r.status_code == 200:
      # Add 'EMC-CSRF-TOKEN' header
      self.headers['EMC-CSRF-TOKEN']=r.headers['EMC-CSRF-TOKEN']
      return True	# Session started
    else:
      return False	# Session not started

  def stopSession(self):
    url = self.base + '/types/loginSessionInfo/action/logout'
    args = {"localCleanupOnly" : "true"}
    self.doPost(url, args)

  def acceptEULA(self):
    url = self.base+"/instances/system/0/action/modify"
    args = {'isEulaAccepted':'true'}
    self.doPost(url, args)

  def updatePassword(self, newPassword):
    url = self.base+'/instances/user/user_' + self.username + '/action/modify'
    args = {'password':newPassword, 'oldPassword':self.password}
    self.doPost(url, args)
    self.password = newPassword

  def updateDnsServers(self, dnsServers):
    url = self.base + '/instances/dnsServer/0'
    params = {'fields':'addresses,domain,origin'}
    status_code, text = self.doGet(url, params)
    if status_code == 200:
      if json.loads(text)["content"]["addresses"] != dnsServers: 
        print("Updating DNS servers...")
        url = self.base + '/instances/dnsServer/0/action/modify'
        args = {'addresses': dnsServers}
        self.doPost(url, args)
        print("Updated DNS servers.")
      else:
        print("DNS servers already set correctly, no update needed.")

  def updateNtpServers(self, ntpServers):
    url = self.base + '/instances/ntpServer/0'
    params = {'fields':'addresses'}
    status_code, text = self.doGet(url, params)
    if status_code == 200:
      if json.loads(text)["content"]["addresses"] != ntpServers: 
        print("Updating NTP servers...")
        url = self.base + '/instances/ntpServer/0/action/modify'
        args = {'addresses': ntpServers, 'rebootPrivilege': 2}
        self.doPost(url, args)
        print("Updated NTP servers.")
      else:
        print("NTP servers already set correctly, no update needed.")

