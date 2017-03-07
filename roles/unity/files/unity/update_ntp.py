import sys, requests, requests.auth, json
from unity_session import UnitySession

host = sys.argv[1]	# Unity server
username = sys.argv[2]	# Unity admin username
password = sys.argv[3]	# Unity admin password
ntpServers = sys.argv[4:]	# List of NTP servers

# Start a new session and update NTP servers
s = UnitySession(host, username, password)
if s.startSession():
  s.updateNtpServers(ntpServers)
  s.stopSession()
