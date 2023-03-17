# ansible-ntp-server

based on gerlingguy NTP role a very smaller version specific for Debian and acoby environment only.


## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    ntp_enabled: true

Whether to start the ntpd service and enable it at system boot. On many virtual machines that run inside a container (like OpenVZ or VirtualBox), it's recommended you don't run the NTP daemon, since the host itself should be set to synchronize time for all its child VMs.

    ntp_timezone: Europe/Berlin

Set the timezone for your server.

    ntp_manage_config: false

The default NTP driftfile should be correct for your distribution, but there are some cases where you may want to override the default.

    ntp_area: 'de'

Specify the NTP servers you'd like to use. Only takes effect if you allow this role to manage NTP's configuration, by setting `ntp_manage_config` to `True`.

    ntp_restrict:
      - "127.0.0.1"
      - "::1"

Restrict NTP access to these hosts; loopback only, by default.

    ntp_cron_handler_enabled: false

Whether to restart the cron daemon after the timezone has changed.

    ntp_tinker_panic: true

Enable tinker panic, which is useful when running NTP in a VM.

## Dependencies

None.

## Example Playbook

    - hosts: all
      roles:
        - acoby.ntp-server

Your inventory needs the var

    ntp_timezone: Europe/Berlin

## License

MIT / BSD

## Author Information

This role was created in 2014 by [Jeff Geerling](https://www.jeffgeerling.com/), author of [Ansible for DevOps](https://www.ansiblefordevops.com/).


## Dependencies

This role need to have acoby.collection to be installed with

    ansible-galaxy collection install git+https://github.com/acoby/ansible-collection.git,main

It contains some mandatory modules and filters.
