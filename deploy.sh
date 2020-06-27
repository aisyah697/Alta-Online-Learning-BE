#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&

source ~/.profile
echo "$DOCKER_PASSWORD" | docker login --username $DOCKER_USERNAME --password-stdin
sudo docker stop be_alta
sudo docker rm be_alta
sudo docker rmi yopiragil/alta:latest
sudo docker run -d --name be_alta -p 5000:5000 yopiragil/alta:latest
