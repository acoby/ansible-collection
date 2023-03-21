#!/bin/bash

host=`hostname -f`
service_file="/srv/docker/services.${host}"

if [ ! -f "${service_file}" ]; then
  echo "Could not find service definition in ${service_file}"
  exit 1
fi

status_services() {
  while IFS= read -r service; do
    echo "Service: ${service}"
    echo ""
    docker-compose -f ${service}/docker-compose.yml ps
    echo ""
  done < "${service_file}"
}

start_services() {
  while IFS= read -r service; do
    echo "Service: ${service}"
    echo ""
    docker-compose -f ${service}/docker-compose.yml up -d
    echo ""
  done < "${service_file}"
}

stop_services() {
  while IFS= read -r service; do
    echo "Service: ${service}"
    echo ""
    docker-compose -f ${service}/docker-compose.yml down
    echo ""
  done < "${service_file}"
}

restart_services() {
  while IFS= read -r service; do
    echo "Service: ${service}"
    echo ""
    ${service}/bin/restart.sh
    echo ""
  done < "${service_file}"
}

update_services() {
  while IFS= read -r service; do
    echo "Service: ${service}"
    echo ""
    ${service}/bin/update.sh
    echo ""
  done < "${service_file}"
}

backup_services() {
  while IFS= read -r service; do
    echo "Service: ${service}"
    echo ""
    ${service}/bin/backup.sh
    echo ""
  done < "${service_file}"
}



case "$1" in
  start)
    start_services
    ;;
  stop)
    stop_services
    ;;
  restart)
    restart_services
    ;;
  update)
    update_services
    ;;
  status)
    status_services
    ;;
  backup)
    backup_services
    ;;
  *)
    echo "Use $0 start|stop|restart|status|backup|update"
    exit 1
    ;;
esac

#eof