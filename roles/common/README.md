# ansible-common

Needs the following vars

  - owner.users[] with
    - username
    - shadow
    - pubkey
    - department
  - inventory.root_password
  - inventory.mail.username
  - inventory.mail.password
  - inventory.mail.host
  - inventory.mail.port
  - inventory.mail.from

## Dependencies

This role need to have acoby.collection to be installed with

    ansible-galaxy collection install git+https://github.com/acoby/ansible-collection.git,main

It contains some mandatory modules and filters.

