import sys, requests, requests.auth, json
from unity_session import UnitySession

cmd = sys.argv[1]	# command to execute
host = sys.argv[2]	# Unity server
username = sys.argv[3]	# Unity admin username
password = sys.argv[4]	# Unity admin password

# Start a new session, update admin user password, and accept EULA
s = UnitySession(host, username, password)
if s.start():
  if cmd == "accept-eula":
    s.acceptEULA()
  elif cmd == "update-password":
    newPassword = sys.argv[5]
    s.updatePassword(newPassword)
  elif cmd == "update-dns":
    dnsServers = sys.argv[5:]
    s.updateDnsServers(dnsServers)
  elif cmd == "update-ntp":
    ntpServers = sys.argv[5:]
    s.updateNtpServers(ntpServers)
  s.stop()
