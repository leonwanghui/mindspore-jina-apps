import numpy as np
from jina.executors.encoders.frameworks import BaseMindsporeEncoder


class MindsporeResNet50(BaseMindsporeEncoder):
    """
    :class:`MindsporeResNet50` Encoding image into vectors using mindspore.
    """

    def encode(self, data, *args, **kwargs):
        from mindspore import Tensor

        data = np.pad(data.reshape([-1, 3, 224, 224]),
                      [(0, 0), (0, 0), (0, 4), (0, 4)]).astype('float32')
        return self.model(Tensor(data)).asnumpy()

    def get_cell(self):
        from .resnet.src.resnet import ResNet50
        class ResNet50Embed(ResNet50):
            def construct(self, x):
                x = self.conv1(x)
                x = self.bn1(x)
                x = self.relu(x)
                c1 = self.maxpool(x)

                c2 = self.layer1(c1)
                c3 = self.layer2(c2)
                c4 = self.layer3(c3)
                c5 = self.layer4(c4)

                out = self.mean(c5, (2, 3))
                out = self.flatten(out)

        return ResNet50Embed()
