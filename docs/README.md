# Ansible Collection - acoby.collection

Documentation for the collection.

## Modules

- acoby.collection.compose - manage docker compose with exec and run
- acoby.collection.define_configuration - manage static yaml based facts configuration per host
- acoby.collection.get_kernel_info - read kernel infos
- acoby.collection.move - idempotent move, replacement for command: mv

## Filters

- urlencode - encode string with urlencode
- quote_wrap - wrap a list of strings with quotes
- service_ipv4_address - define a acoby specific network range for services
- service_ipv6_address - define a acoby specific network range for services

## Roles

- acoby.collection.common - a base role for all systems
- acoby.collection.fail2ban - a role for managing fail2ban (requires acoby.collection.common)
- acoby.collection.ssh - a role for managing SSH (requires acoby.collection.fail2ban)
- acoby.collection.firewall - a role for managing a iptables based firewall (requires acoby.collection.ssh)
- acoby.collection.icinga_agent - a role for managing an icinga agent (requires acoby.collection.firewall)
- acoby.collection.pan - a role for managing a private area network between all hosts in a cluster (requires acoby.collection.icinga_agent)

- acoby.collection.ca_server - a role for managing a CA provider instance (requires acoby.collection.common)
- acoby.collection.gfs_client - a role for managing a GlusterFS client (requires acoby.collection.pan)
- acoby.collection.gfs_server - a role for managing a GlusterFS server (requires acoby.collection.pan)
- acoby.collection.nfs_client - a role for managing a NFS client (requires acoby.collection.pan)
- acoby.collection.nfs_server - a role for managing a NFS server (requires acoby.collection.pan)
- acoby.collection.ntp_server - a role for managing a NTP server (requires acoby.collection.pan)
- acoby.collection.bind - a role for managing a DNS server (requires acoby.collection.pan)
- acoby.collection.docker - a role for managing Docker (requires acoby.collection.pan)

So any higher role then

- requires acoby.collection.pan, which
- requires acoby.collection.icinga_agent, 
- requires acoby.collection.firewall, which 
- requires acoby.collection.ssh, which 
- requires acoby.collection.fail2ban, which 
- requires acoby.collection.common.

Any host then is guaranteed to have correct network setup with fail2ban, firewall, icinga agent and a PAN network defined.
