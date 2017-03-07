import sys, requests, requests.auth, json
from unity_session import UnitySession

host = sys.argv[1]	# Unity server
username = sys.argv[2]	# Unity admin username
oldPassword = sys.argv[3]	# Unity admin password
newPassword = sys.argv[4]

# Start a new session and accept EULA
s = UnitySession(host, username, oldPassword)
if s.startSession():
  s.updatePassword(newPassword)
  s.stopSession()
