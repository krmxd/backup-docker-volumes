import os
from br_docker_volume import setup_client, backup_volume, get_containers

CONTAINER_NAME = os.getenv('CONTAINER_NAME')
BACKUP_LOCATION = os.environ.get('BACKUP_LOCATION')
DOCKER_SOCK = os.environ.get('DOCKER_SOCK')

if CONTAINER_NAME is None:
    raise ValueError("CONTAINER_NAME IS MANDATORY")

if BACKUP_LOCATION is None:
    BACKUP_LOCATION = "/backup"

if DOCKER_SOCK is None:
    DOCKER_SOCK = 'unix://var/run/docker.sock'

container_list = [c.upper() for c in CONTAINER_NAME.split(" ")]

if not container_list:
    exit(1)

client = setup_client(DOCKER_SOCK)
all_container = get_containers(client)

if "ALL" in container_list:
    for c in all_container:
        backup_operation = backup_volume(client, c, BACKUP_LOCATION)
        if backup_operation is not None:
            print(f"{c} backup completed: {backup_operation}")

else:
    for c in container_list:
        if c not in all_container:
            print(f"ERROR: {c} is not found on the system")
        else:
            backup_operation = backup_volume(client, CONTAINER_NAME, BACKUP_LOCATION)
            if backup_operation is not None:
                print(f"{c} backup completed: {backup_operation}")
exit(0)
