import sys, requests, requests.auth, json
from unity_session import UnitySession

host = sys.argv[1]	# Unity server
username = sys.argv[2]	# Unity admin username
password = sys.argv[3]	# Unity admin password

# Start a new session, update admin user password, and accept EULA
s = UnitySession(host, username, password)
if s.startSession():
  s.acceptEULA()
  s.stopSession()
