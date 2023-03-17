# ansible_icinga_agent

## vars

## add machine without agent

    addgroup nagios
    adduser --home /var/lib/nagios --shell /bin/bash --disabled-password --system --ingroup nagios nagios
    apt install sudo
    echo 'nagios ALL=(root) NOPASSWD:/usr/lib/nagios/plugins/check_*' > /etc/sudoers.d/90-icinga-user
    mkdir -p /var/lib/nagios/.ssh
    echo 'ssh-rsa ...' > /var/lib/nagios/.ssh/authorized_keys
    chown -R nagios:nagios /var/lib/nagios/.ssh
    chmod 400 /var/lib/nagios/.ssh/authorized_keys
    mkdir -p /usr/lib/nagios/plugins /var/cache/nagios
    apt install bc sysstat monitoring-plugins-basic libmonitoring-plugin-perl
    # scp /usr/lib/nagios/plugins/* user@server:/usr/lib/nagios/plugins/.

## Dependencies

This role need to have acoby.collection to be installed with

    ansible-galaxy collection install git+https://github.com/acoby/ansible-collection.git,main

It contains some mandatory modules and filters.
