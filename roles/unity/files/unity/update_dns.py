import sys, requests, requests.auth, json
from unity_session import UnitySession

host = sys.argv[1]	# Unity server
username = sys.argv[2]	# Unity admin username
password = sys.argv[3]	# Unity admin password
dnsServers = sys.argv[4:]	# List of DNS servers

# Start a new session and update DNS servers
s = UnitySession(host, username, password)
s.startSession():
  s.updateDnsServers(dnsServers)
  s.stopSession()
