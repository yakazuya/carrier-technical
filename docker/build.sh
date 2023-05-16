#!/bin/bash

BUILD_DIR=$(dirname $(readlink -f $0))/src
USER_ID=$(id -u)

IMAGE_NAME="carrier-technical:ubuntu2204"

docker build \
  -t ${IMAGE_NAME} \
  -f ${BUILD_DIR}/Dockerfile \
  --build-arg UID=$(id -u) \
  --build-arg GID=$(id -g) \
  ${BUILD_DIR}