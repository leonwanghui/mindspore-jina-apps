__copyright__ = "Copyright (c) 2020 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import numpy as np
from jina.executors.encoders.frameworks import BaseMindsporeEncoder
from jina.executors.crafters.image.io import ImageReader
from jina.executors.decorators import batching
from ..lenet import LeNet5

import sys
sys.path.append('..')


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

    @batching
    def encode(self, data, *args, **kwargs):
        from mindspore import Tensor
        return self.model(Tensor(data[:, 0:1, :, :].astype('float32'))).asnumpy()

    def get_model(self):
        return LeNet5Feat()


class MnistImageReader(ImageReader):
    def craft(self, blob, *args, **kwargs):
        # convert buffer to blob
        return dict(weight=1., blob=np.stack([blob.reshape(28, 28) for _ in range(3)]))
