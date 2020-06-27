#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&

source ~/.profile
echo "$DOCKER_PASSWORD" | docker login --username $DOCKER_USERNAME --password-stdin
docker stop be_alta
docker rm be_alta
docker rmi yopiragil/alta:latest
docker run -d --name be_alta -p 5000:5000 yopiragil/alta:latest
