#!/bin/sh

cd /workdir
echo "Running backup routine to backup docker volumes... (`date`)"
docker compose run backupvolumes
