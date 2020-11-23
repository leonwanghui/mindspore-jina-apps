import numpy as np
from .. import LeNetImageEncoder


def test_mindsporelenet():
    """here is my test code

    https://docs.pytest.org/en/stable/getting-started.html#create-your-first-test
    """
    mln = LeNetImageEncoder('../lenet/ckpt/checkpoint_lenet-1_468.ckpt')
    tmp = np.random.random([4, 28 * 28])

    # The sixth layer is a fully connected layer (F6) with 84 units.
    # it is the last layer before the output
    assert mln.encode(tmp).shape == (4, 84)
