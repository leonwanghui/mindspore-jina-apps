# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
import os
import struct
import argparse
import numpy as np
from PIL import Image


def load_mnist(dir_path, kind='train'):
    """Load MNIST Dataset from the given path"""
    labels_path = os.path.join(dir_path, '%s-labels-idx1-ubyte' % kind)
    images_path = os.path.join(dir_path, '%s-images-idx3-ubyte' % kind)
    with open(labels_path, 'rb') as labels_file:
        magic, num = struct.unpack('>II', labels_file.read(8))
        labels = np.fromfile(labels_file, dtype=np.uint8)
    with open(images_path, 'rb') as images_file:
        magic, num, rows, cols = struct.unpack(">IIII", images_file.read(16))
        images = np.fromfile(images_file, dtype=np.uint8)
    return images, labels, num


def save_mnist_to_jpg(images, labels, save_dir, kind, num):
    """Convert and save the MNIST dataset to.jpg image format"""
    one_pic_pixels = 28 * 28
    for i in range(num):
        img = images[i * one_pic_pixels:(i + 1) * one_pic_pixels]
        img_np = np.array(img, dtype=np.uint8).reshape(28, 28)
        label_val = labels[i]
        jpg_name = os.path.join(save_dir, '{}_{}_{}.jpg'.format(kind, i, label_val))
        Image.fromarray(img_np).save(jpg_name)
        print('{} ==> {}_{}_{}.jpg'.format(i, kind, i, label_val))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="MNIST Dataset Operations")
    parser.add_argument('--data_dir', type=str, default='/root/jina/chinese-mnist', help='MNIST dataset dir')
    parser.add_argument('--kind', type=str, default='train', help='MNIST dataset: train or t10k')
    parser.add_argument('--save_dir', type=str, default='/root/jina/chinese-mnist/jpg', help='used to save mnist jpg')
    args = parser.parse_args()

    if not os.path.exists(args.data_dir):
        os.makedirs(args.data_dir)

    images_np, labels_np, kind_num = load_mnist(args.data_dir, args.kind)

    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    save_mnist_to_jpg(images_np, labels_np, args.save_dir, args.kind, kind_num)
