__copyright__ = "Copyright (c) 2020 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import io
import numpy as np
from typing import Dict
from PIL import Image
from jina.executors.encoders.frameworks import BaseMindsporeEncoder
from jina.executors.crafters import BaseCrafter

from .lenet.src.lenet import LeNet5


class LeNet5Feat(LeNet5):
    def construct(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.max_pool2d(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.max_pool2d(x)
        x = self.flatten(x)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        return x


class LeNetImageEncoder(BaseMindsporeEncoder):
    def encode(self, data, *args, **kwargs):
        from mindspore import Tensor
        data = np.pad(data.reshape([-1, 1, 28, 28]),
                              [(0, 0), (0, 0), (0, 4), (0, 4)]).astype('float32')
        return self.model(Tensor(data)).asnumpy()

    def get_cell(self):
        return LeNet5Feat()


class MnistImageReader(BaseCrafter):
    """
    :class:`MnistImageReader` loads the image from the given file path and save the `ndarray` of the image in the Document.
    """

    def __init__(self, channel_axis: int = -1, *args, **kwargs):
        """
        :class:`MnistImageReader` load an image file and craft into image matrix.

        :param channel_axis: the axis id of the color channel, ``-1`` indicates the color channel info at the last axis
        """
        super().__init__(*args, **kwargs)
        self.channel_axis = channel_axis

    def craft(self, buffer: bytes, uri: str, *args, **kwargs) -> Dict:
        """
        Read the image from the given file path that specified in `buffer` and save the `ndarray` of the image in
            the `blob` of the document.

        :param buffer: the image in raw bytes
        :param uri: the image file path
        """
        if buffer:
            raw_img = Image.open(io.BytesIO(buffer))
        elif uri:
            raw_img = Image.open(uri)
        else:
            raise ValueError('no value found in "buffer" and "uri"')
        raw_img = raw_img.convert('1')
        img = np.array(raw_img).astype('float32')
        if self.channel_axis != -1:
            img = np.moveaxis(img, -1, self.channel_axis)
        return dict(weight=1., blob=img)
