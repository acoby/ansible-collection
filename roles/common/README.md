# ansible-common

Needs the following vars

- owner.users[] with
  - username
  - shadow
  - pubkey
  - department
- inventory.root_password
- inventory.network.pan.ipv4
- inventory.network.pan.ipv6
- inventory.network.lan.ipv4
- inventory.network.lan.ipv6
- inventory.networks[]
- hostvars[groups['all']].network.wan.ipv4
- hostvars[groups['all']].network.wan.ipv6
- inventory.mail.username
- inventory.mail.password
- inventory.mail.host
- inventory.mail.port
- inventory.mail.recipient
- inventory.mail.from
- inventory.monitoring.notification.acoby.endpoint
- inventory.monitoring.notification.acoby.username
- inventory.monitoring.notification.acoby.password

## Dependencies

This role need to have acoby.collection to be installed with

    ansible-galaxy collection install git+https://github.com/acoby/ansible-collection.git,main

It contains some mandatory modules and filters.

