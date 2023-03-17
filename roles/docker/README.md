# Docker role

wir teilen die Docker Rolle mittlerweile auf in die verschiedenen Lösungen. 

Eigentlich müsste die Rolle "sandbox" heißen, weil wir die Sandboxing Lösung
auf Basis der Host-Property infrastructure.software.sandbox installieren.

Default ist im Moment noch docker-ce. Alternativ existiert podman.

## Docker-Ce

Die Community Edition von Docker war lange Zeit der Quasistandard. Leider ist
durch wirtschaftliche Schieflage und einige technische Unzulänglichkeiten die
Community am Abwandern. Die Software stirbt. Ob das gefühlt ist, weiß ich nicht.

Auf jeden Fall ist der IPv6 Netzwerk-Stack undurchsichtig und wirkt drangeklatscht.

## Podman

Podman basiert auf einer Umsetzung von RedHat. Sie kann rootless betrieben werden,
was im Netzwerk einige Implikationen hat. Vorteil von Podman ist, dass es komplett
auf Community Lösungen aufsetzt (was immer das heißt). Weiterer Vorteil speziell für
uns ist, dass es IPv6only betrieben werden kann. Das Netzwerk lässt sich ab v2 deutlich
einfacher konfigurieren. Nachteil ist, dass es immer noch an einigen Stellen in
Relation zu docker-ce hackt.

- https://www.cni.dev/plugins/ipam/host-local/
  Details über den Aufbau von Netzwerken im Bridge-Mode.
  
## Vars

- infrastructure.software.sandbox
- network.wan.interface
- network.pan.interface
- network.wan.ipv4.dns[] with
  - list of IPv4 DNS servers
- network.wan.ipv6.dns[] with
  - list of IPv6 DNS servers
- inventory.registries[] with
  - name
  - user
  - pass
- docker_service_dependencies[] with list of systemd service names


## Dependencies

This role need to have acoby.collection to be installed with

    ansible-galaxy collection install git+https://github.com/acoby/ansible-collection.git,main

It contains some mandatory modules and filters.
