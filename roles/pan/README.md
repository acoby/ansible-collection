# ansible-pan

## vars

- acoby_pan_port
- network.pan.interface
- network.pan.ipv4.address
- network.pan.ipv6.address
- network.pan.private_key
- hostvars[groups['pan']].network.pan.public_key


## Dependencies

This role need to have acoby.collection to be installed with

    ansible-galaxy collection install git+https://github.com/acoby/ansible-collection.git,main

It contains some mandatory modules and filters.
