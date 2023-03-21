# Ansible Collection - acoby.collection

Documentation for the collection.

## Modules

- `acoby.collection.compose` - manage docker compose with exec and run
- `acoby.collection.configuration` - manage static yaml based facts configuration per host
- `acoby.collection.get_kernel_info` - read kernel infos
- `acoby.collection.move` - idempotent move, replacement for command: mv

## Filters

- `acoby.collection.urlencode` - encode string with urlencode
- `acoby.collection.quote_wrap` - wrap a list of strings with quotes
- `acoby.collection.service_ipv4_address` - define a acoby specific network range for services
- `acoby.collection.service_ipv6_address` - define a acoby specific network range for services

## Roles

- `acoby.collection.common` - a base role for all systems, contains common, fail2ban, ssh, firewall

- `acoby.collection.backup_client` - a role for managing a backup client (requires `acoby.collection.common`)
- `acoby.collection.bind` - a role for managing a DNS server (requires `acoby.collection.common`)
- `acoby.collection.ca_client` - a role for managing a CA client instance (requires `acoby.collection.common`)
- `acoby.collection.ca_server` - a role for managing a CA provider instance (requires `acoby.collection.common`)
- `acoby.collection.gfs_client` - a role for managing a GlusterFS client
- `acoby.collection.gfs_server` - a role for managing a GlusterFS server (requires `acoby.collection.common`)
- `acoby.collection.icinga_agent_check` - a role for managing custom icinga checks (requires `acoby.collection.common`)
- `acoby.collection.nfs_client` - a role for managing a NFS client
- `acoby.collection.nfs_server` - a role for managing a NFS server (requires `acoby.collection.common`)
- `acoby.collection.ntp_server` - a role for managing a NTP server (requires `acoby.collection.common`)
- `acoby.collection.sandbox` - a role for managing Docker (requires `acoby.collection.common`, `acoby.collection.nfs_client` and `acoby.collection.gfs_client`)

So any higher role then should require `acoby.collection.common`.
Any host is guaranteed to have correct network setup with fail2ban, firewall, icinga agent, backup and a PAN network defined.

## Inventory

The acoby roles are depending on a complex inventory, which describes a lot of informations over all systems and states

A host should have the following facts:

- `hardware.type` - contains either "virtual" or "physical" which is relevant for managing hardware configuration. Ony virtal machine can be configured
- `infrastructure.os` - contains the concrete software version of the operating system, like "debian-11"
- `infrastructure.hostType` - could be "vm" or "host" 
- `infrastructure.type` - a product information from the underlying provider, a string without any function (for monitoring grouping)
- `infrastructure.location` - the computer center, where this system is located - for monitoring grouping) 
- `infrastructure.hostname` - a short but static name of this host - because some provider do not allow renaming of systems 
- `infrastructure.parent` - for monitoring, either "master" which means, it depends on the monitoring master or another host means, it depends to that host 
- `infrastructure.provider.type` - currently we support "hetzner-root", "hetzner-cloud" and "on-promise" 
- `infrastructure.provider.ipv4.dns` - a list of public DNS servers from the provider itself
- `infrastructure.provider.ipv6.dns` - a list of public DNS servers from the provider itself
- `infrastructure.software.sandbox` - either "docker-ce" or "podman", used to configure container solution
- `owner.customerId` - a reference to the dict in inventory under "owners.<customerId>"
- `network.wan` - a mandatory dictionary describing the world area network connectivity of this host
- `network.wan.fqdn` - the FQDN of this host
- `network.wan.interface` - the physical interface of this host (like "eth0" or "ens18") 
- `network.wan.ipv4.address` - the public IPv4 address, when available (we support IPv4 only and DualStack and IPv6 only)
- `network.wan.ipv4.netmask` -  the netmask for the public IPv4 address
- `network.wan.ipv4.gateway` - the gateway for this public IPv4 address
- `network.wan.ipv4.dns` - a list of IPv4 DNS servers for this host 
- `network.wan.ipv6.address` - the public IPv6 address, when available (we support IPv4 only and DualStack and IPv6 only)
- `network.wan.ipv6.prefix` -  the netmask for the public IPv6 address
- `network.wan.ipv6.gateway` - the gateway for this public IPv6 address
- `network.wan.ipv6.dns` - a list of IPv6 DNS servers for this host 
- `network.pan` - a mandatory dictionary for a private area network (PAN) over either LAN or WAN addresses
- `network.pan.fqdn` - the FQDN of this host inside the private area network (PAN)
- `network.pan.interface` - the Wiregate interface of this host (like "wg0") 
- `network.pan.ipv4.address` - the PAN IPv4 address, when available (we support DualStack PAN only)
- `network.pan.ipv4.netmask` -  the netmask for the PAN IPv4 address
- `network.pan.ipv4.gateway` - the gateway for this PAN IPv4 address
- `network.pan.ipv4.dns` - a list of IPv4 DNS servers for this host 
- `network.pan.ipv6.address` - the PAN IPv6 address, when available (we support DualStack PAN only)
- `network.pan.ipv6.prefix` -  the netmask for the PAN IPv6 address
- `network.pan.ipv6.gateway` - the gateway for this PAN IPv6 address
- `network.pan.ipv6.dns` - a list of IPv6 DNS servers for this host 
- `network.lan` - an optional dict for a LAN network between all systems
- `network.lan.fqdn` - the FQDN of this host inside the local area network (LAN)
- `network.lan.interface` - the local interface of this host (like "eth1") 
- `network.lan.private_key` - the private key for Wireguard
- `network.lan.public_key` - the public key for Wireguard
- `network.lan.ipv4.address` - the LAN IPv4 address, when available (we support DualStack LAN only)
- `network.lan.ipv4.netmask` -  the netmask for the LAN IPv4 address
- `network.lan.ipv4.gateway` - the gateway for this LAN IPv4 address
- `network.lan.ipv4.dns` - a list of IPv4 DNS servers for this host 
- `network.lan.ipv6.address` - the LAN IPv6 address, when available (we support DualStack LAN only)
- `network.lan.ipv6.prefix` -  the netmask for the LAN IPv6 address
- `network.lan.ipv6.gateway` - the gateway for this LAN IPv6 address
- `network.lan.ipv6.dns` - a list of IPv6 DNS servers for this host

And the underlying inventory for all group contains some informations about the given infrastructure.

- `acoby_pan_port` - the UDP port for the private area network for the whole infrastructure
- `customers` - a dictionary for all customers within this inventory (owners of hosts and services)
- `customers.<customerId>.name` - Name of custmer
- `customers.<customerId>.company` - Name of company
- `customers.<customerId>.country` - Country code
- `customers.<customerId>.contact` - a name for a contact person
- `customers.<customerId>.email` - an email address for verification
- `customers.<customerId>.email_notificatio` - an email address for monitoring alerts
- `inventory_user` - the username to use to login to the host, is created during bootstrap and replaces ansible_user
- `inventory_pass` - the password for the user, which is set during bootstrap and used for sudo
- `inventory` - a dictionary with generic informations of the inventory
- `inventory.id` - must be defined except for molecule tests 
- `inventory.customerId` - a link to the customer, which belongs to this inventory
- `inventory.name` - a name of this inventory for readable reasons only
- `inventory.domain` - deprecated - a domain for the inventory, replaced by fqdn on all objects
- `inventory.local_domain` - deprecated - a local domain for the inventory, replaced by inventory.network.lan.domain
- `inventory.root_password` - the password for the root user 
- `inventory.backup` -a reference to the backup server instance
- `inventory.monitoring` - a dictionary to inform the inventory about the monitoring master
- `inventory.monitoring.id` - a reference to the monitoring master service instance within the cluster 
- `inventory.monitoring.master` - a hostname within the inventory containing the service instance 
- `inventory.monitoring.master_domain` - a public available domain for URL generation
- `inventory.monitoring.endpoint` - an endpoint of the API for URL generation 
- `inventory.monitoring.username` - a username for the monitoring API
- `inventory.monitoring.password` - a password for the monitoring API
- `inventory.monitoring.port` - the port of the master instance
- `inventory.monitoring.notification.acoby.endpoint` - the endpoint of nobod notification
- `inventory.monitoring.notification.acoby.username` - the username for nobod
- `inventory.monitoring.notification.acoby.password` - the password for nobod
- `inventory.monitoring.notification.rocketchat.webhook` - the webhook URL for rocketchat notification
- `inventory.mail` - a dictionary to present the inventoary a central mail system for communication
- `inventory.mail.host` - the host name of the SMTP server
- `inventory.mail.port` - the port name of the SMTP server, like "25", "587"
- `inventory.mail.username` - the username to login to the SMTP server, we do not allow open relays
- `inventory.mail.password` - the password to login to the SMTP server, we do not allow open relays
- `inventory.mail.name` - a human readable default name of the sender (like "acoby Bot")
- `inventory.mail.from` - the mail address to use as from
- `inventory.mail.recipient` - the fallback email address for notifications
- `inventory.network.pan` - defines some mandatory informations for the PAN network
- `inventory.network.pan.domain` - the domain of the PAN network like "domain.pan"
- `inventory.network.pan.ipv4` - the IPv4 network range of the PAN
- `inventory.network.pan.ipv6` - the IPv6 network range of the PAN
- `inventory.network.lan` - defines some mandatory informations, when there is a LAN network (only relevant, when defined)
- `inventory.network.lan.domain` - the domain of the LAN network, like "domain.lan"
- `inventory.network.lan.ipv4` - the IPv4 network range of the LAN
- `inventory.network.lan.ipv6` - the IPv6 network range of the LAN
- `ntp_area` - an area (like "de") for the NTP server pool
- `ntp_timezome` - a timezone for the inventory (asuming all hosts are in one timezone)
- `users` - a dictionary of users that should be present on all systems
- `users[].username` - the username of the user to create 
- `users[].roles` - a string containing either "REPORT", "USER" or "ADMIN", only admins can make sudo 
- `users[].customerId` - reference to customer dictionary 
- `users[].department` - information for passwd 
- `users[].pubkey` - a public key, to login via SSH 
- `users[].shadow` - a hash of the users password

Also we have a special structure for all services. They are stored in the general inventory dictionary

- `inventory.registries` - a list of Docker registries with `name`, `type="docker"`, `user` and `pass` keys
- `inventory.networks` - a list of optional external networks to allow full access to the inventory
- `inventory.storages` - a list of external storages (for backup volumes)
- `inventory.services` - a dictionary for describing all available services
- `inventory.instances` - a dictionary for describing all available service instances

## Known issues

- we need to check, that infrastructure server are configred first (Proxmox, DNS, Storage)
- resolv.conf is filled with public WAN DNS entries (always) but should use PAN DNS, when available
- Proxmox Hosts should provide DHCP for local VMs
