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

- acoby.common - a base role for all systems
- acoby.fail2ban - a role for managing fail2ban (requires acoby.common)
- acoby.ssh - a role for managing SSH (requires acoby.fail2ban)
- acoby.firewall - a role for managing a iptables based firewall (requires acoby.ssh)
- acoby.icinga_agent - a role for managing an icinga agent (requires acoby.firewall)
- acoby.pan - a role for managing a private area network between all hosts in a cluster (requires acoby.icinga\_agent)
- acoby.ntp_server - a role for managing an NTP server (requires acoby.pan)
- acoby.bind - a role for managing a DNS server (requires acoby.pan)
- acoby.docker - a role for managing Docker (requires acoby.pan)

So any higher role then requires acoby.pan, which requires acoby.icinga_agent, which requires acoby.firewall, which requires acoby.ssh, which requires acoby.fail2ban, which requires acoby.common.
Any host then is guaranteed to have correct network setup with fail2ban, firewall, icinga agent and a PAN network defined.

## Missing

currently we miss roles for

- managing mount points (local, NFS, GFS, SSHFS)

