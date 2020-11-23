#!/bin/sh

set -e

DATA_DIR=/tmp/jina/chinese-mnist

if [ -d ${DATA_DIR} ]; then
  echo ${DATA_DIR}' exists, please remove it before running the script'
  exit 1
fi

mkdir -p ${DATA_DIR}
cd ${DATA_DIR}

wget -P ${DATA_DIR} https://mnist-jina.obs.cn-north-4.myhuaweicloud.com/train-images-idx3-ubyte
wget -P ${DATA_DIR} https://mnist-jina.obs.cn-north-4.myhuaweicloud.com/train-labels-idx1-ubyte
