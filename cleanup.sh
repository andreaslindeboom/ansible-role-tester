#!/usr/bin/env bash
docker rm -f $(docker ps -aq)
docker network rm role_tester_network
docker volume rm keys
docker volume create keys

