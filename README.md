## EMC Unity Configuration and Management

- Requires Ansible 2.2 or newer
- Expects a CentOS/RHEL 7 jump host

These playbooks configures and manages EMC Unity storage appliance.
To use them, first edit the "hosts" inventory file to contain the
hostnames of the jump host on which you want to run programs that 
interact with the Unity system, and edit the group_vars/all file to 
set any Unity configuration parameters you need.

Then run the playbook, like this:

	ansible-playbook -i hosts site.yml

When the playbook run completes, you should be able to see the Unity system 
running with the configuration parameters that you set.

Currently, the playbook only handles the following configurations:

- Accept Unity EULA
- Update default admin user password
- Update DNS server list
- Update NTP server list

If the Unity system time is more than 1000 seconds different from the NTP servers, 
a restart of the Unity system is going to be initiated. The system will be offline 
for a while and then become available again.

This is a very simple playbook and could serve as a starting point for more
complex Unity management tasks. 

The following configurations are to be added to the playbook soon:

- Pool Creation
..* Protection Scheme
..* Select Drives for pool
..* Set compression/dedupe settings
- Alternative Admin Account
- Alternative Admin Password
- Licensing
- ESRS Setup
- Logging settings
- Others as needed to finish initial configuration

The following configuration tasks are to be added to the playbook at a later stage:
- Configure host registration
- Configure luns and add to storage groups
- Configuring correct path options
- Check current configuration against configuration best practices
- Host type settings
- Others as needed

