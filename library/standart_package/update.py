def runUpdate(self, update):
    paramKeys = ['language', 'timeout']
    urlKeys = ['resource_type', 'id', 'action', 'attributes', 'filter'] + paramKeys
    params = {key: update[key] for key in update if key in paramKeys}
    args = {key: update[key] for key in update if key not in urlKeys}
    msg = {}

    if 'resource_type' in update:  # A resource must have the "resource_type" parameter
        msg['resource_type'] = update['resource_type']
    else:
        self.err = {'error': 'Update has no "resource_type" parameter', 'update': update}
        self.exitFail()

    if 'id' in update:  # Update an existing resource instance with ID
        msg['id'] = update['id']
        url = '/api/instances/' + update['resource_type'] + '/' + update['id'] + '/action/' + update.get('action',
                                                                                                         'modify')
        if 'action' not in update:
            update['action'] = 'modify'  # default action
            msg['action'] = update['action']
            if self.isDuplicate(update):
                msg['warn'] = 'The existing instances already has the same attributes as the update operation. ' \
                              'No update will happen.'
                self._changeResult(None, url, args, changed=False, msg=msg, params=params)
                return
        elif update['action'] == 'delete':
            msg = update
            url = '/api/instances/' + update['resource_type'] + '/' + update['id']
            if not self.isDuplicate(update):
                msg['warn'] = 'The instance to be deleted does not exist. No update will happen.'
                self._changeResult(None, url, args, changed=False, msg=msg, params=params)
                return
            else:
                resp = self._doDelete(url, msg)
                return
    else:
        if 'action' in update:  # Class-level action
            url = '/api/types/' + update['resource_type'] + '/action/' + update['action']
        else:
            update['action'] = 'create'  # Create a new instance
            msg['action'] = update['action']
            url = '/api/types/' + update['resource_type'] + '/instances'
            if self.checkMode:  # Only check duplicate entries during check mode. The users accept the consequences if they still want to add the new instance
                duplicates = self.isDuplicate(update)
                if duplicates:
                    msg.update({
                        'warn': 'Instances with the same attributes already exist for the creation operation. Create the new instance at your own risk.',
                        'duplicates': duplicates})
                    self._changeResult(None, url, args, changed=False, msg=msg, params=params)
                    return
    msg['action'] = update['action']
    resp = self._doPost(url, args, params=params, msg=msg)