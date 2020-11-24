#!/bin/sh

set -e

DATA_DIR=${DATA_DIR:-/root/jina/mushrooms}

if [ -d ${DATA_DIR} ]; then
  echo ${DATA_DIR}' exists, please remove it before running the script'
  exit 1
fi

mkdir -p ${DATA_DIR}
cd ${DATA_DIR}

wget -P ${DATA_DIR} --no-check-certificate https://ascend-tutorials.obs.cn-north-4.myhuaweicloud.com/resnet-50/mushrooms/mushrooms.zip

unzip mushrooms.zip && rm mushrooms.zip
