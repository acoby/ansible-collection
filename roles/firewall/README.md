# ansible-firewall

## vars

- hardware.type != 'physical'
- network.lan.interface
- network.pan.interface
- network.wan.interface
- network.wan.ipv4.dns - port 53
- network.wan.ipv6.dns - port 53
- hostvars[groups['all']].network.wan.interface
- hostvars[groups['all']].network.wan.ipv4.address
- hostvars[groups['all']].network.wan.ipv6.address
- firewall_allow_ipv4[]
  - range
  - port
  - protocol
- firewall_allow_ipv6[]
  - range
  - port
  - protocol

- groups['monitoring'] - port 5665

## Dependencies

This role need to have acoby.collection to be installed with

    ansible-galaxy collection install git+https://github.com/acoby/ansible-collection.git,main

It contains some mandatory modules and filters.
