import argparse
import json
import tarfile
import os
from datetime import datetime
from typing import List, Union

import docker
from docker import APIClient


# test for the running environment using env var. So future changes won't break code.
def running_within_docker() -> bool:
    if os.environ.get('RUNS_IN_DOCKER') is None:
        return False
    else:
        return True


# backup volume logic
def backup_volume(d_client: APIClient, container_name: str, mounted_backup_location: str) -> Union[str, None]:
    container_data = d_client.inspect_container(container_name)

    backup_list = []
    for mount in container_data['Mounts']:
        if mount['Type'] != 'volume':
            continue
        else:
            backup_list.append(mount['Source'])

    if not backup_list:
        return

    print(f"[{container_name}] Adding following volumes to backup: {backup_list}")
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    if running_within_docker():
        tar_path = f"{mounted_backup_location}/{date_time}_{container_name}.tar.gz"
    else:
        tar_path = f"{date_time}_{container_name}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as backup_file:
        for volume in backup_list:
            backup_file.add(volume)
        with open(f'{container_name}_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(container_data, f)
        backup_file.add(f'{container_name}_metadata.json')

    return tar_path


# get container logic
def get_containers(d_client: APIClient) -> List[str]:
    all_container = d_client.containers(all=True)
    container_list = [c['Names'][0][1:] for c in all_container]
    return container_list


# docker client logic
def setup_client(sock: str) -> APIClient:
    docker_client = docker.APIClient(base_url=sock)
    return docker_client


if __name__ == "__main__":

    # setting up argparser
    parser = argparse.ArgumentParser()
    parser.add_argument('--container-name', type=str, required=True)
    parser.add_argument('--backup-location', type=str, required=False, default="/backup")
    parser.add_argument('--docker-sock', type=str, required=False, default='unix://var/run/docker.sock')
    args = parser.parse_args()

    # mapping arguments
    backup_location = args.backup_location
    target_container = args.container_name
    mode = args.mode
    docker_sock = args.docker_sock

    client = setup_client(docker_sock)
    backupped_file = backup_volume(client, target_container, backup_location)
    print(f"Backup file: {backupped_file}")
