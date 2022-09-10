# backup-docker-volumes
python solution for backup and restore of docker volumes

## How it works
Edit the `config.env` to match your container names, or use ALL

```
# Use ALL for backing up all container with volumes.
CONTAINER_NAME = "YOUR_CONTAINER_NAME1 YOUR_CONTAINER_NAME2"
BACKUP_LOCATION = "/backup"
DOCKER_SOCK = 'unix://var/run/docker.sock'
RUNS_IN_DOCKER = "True"
```

Change the `docker-compose.yml` if you want to mount a fileshare or a different location.
By default, the backups are located in /tmp.
```
      - /tmp:/backup
```

:warning: Keeping your backups on the same host doesn't sound like the greatest idea in the world


## Run using docker compose

```
docker compose up
```
