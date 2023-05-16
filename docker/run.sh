#!/bin/bash

USER_ID=$(id -u)
# XSOCK="/tmp/.X11-unix"
# XAUTH="/tmp/.docker.xauth"

HOST_WS=$(dirname $(dirname $(readlink -f $0)))
DOCKER_VOLUME="${DOCKER_VOLUME} -v ${HOST_WS}:/home/carrier-technical/:rw"

DOCKER_ENV="-e XAUTHORITY=${XAUTH}"
DOCKER_ENV="${DOCKER_ENV} -e DISPLAY=$DISPLAY"
# Window System上でQtアプリケーションを実行する際に使用される環境変数の1つ＝＞QtはX11のMIT-SHM拡張を使用しないように設定
DOCKER_ENV="${DOCKER_ENV} -e QT_X11_NO_MITSHM=1"
DOCKER_ENV="${DOCKER_ENV} -e USER_ID=${USER_ID}"
DOCKER_ENV="${DOCKER_ENV} -e HOME=/home/carrier-technical/"
IMAGE_NAME="carrier-technical:ubuntu2204"

DOCKER_IMAGE="${IMAGE_NAME}"


docker run \
  --rm \
  -it \
  --privileged \
  --name ubuntu \
  --net "host" \
  --shm-size 10gb \
  --user root \
  ${DOCKER_ENV} \
  ${DOCKER_VOLUME} \
  ${DOCKER_IMAGE} \
  bash
