from update import runUpdate
def create_iscsi_potal(params):
    ethPort = params['ethernetPort']
    ipAddress = params['ipAddress']
    netmask = params['netmask']
    update = {'resource_type': 'iscsiPortal', 'ethernetPort': ethPort, 'ipAddress': ipAddress,"netmask": netmask}
    runUpdate(update)

