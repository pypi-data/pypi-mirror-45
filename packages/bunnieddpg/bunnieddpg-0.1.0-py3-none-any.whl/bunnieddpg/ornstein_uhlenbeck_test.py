import unittest

import numpy as np
from bunnieddpg.ornstein_uhlenbeck import ornstein_uhlenbeck


class OrnsteinUhlenbeckTest(unittest.TestCase):
  """Tests for ornstein_uhlenbeck function."""

  def setUp(self):
    """Initializes random seed to be 0.

    All test cases are deterministic since random seed is initialized during set up. However, the
    assertion is done using 95 condifidence interval to make sure the reader understand that
    ornstein uhlenbeck function does return a random value.
    """
    np.random.seed(0)

  def test_ornstein_uhlenbeck_zero_should_produce_positive_result(self):
    result = ornstein_uhlenbeck(x=0, mu=0, theta=0.15, sigma=0.2)

    # Assert using 95 condifidence interval.
    self.assertGreaterEqual(result, -0.4)
    self.assertLessEqual(result, 0.4)

  def test_ornstein_uhlenbeck_one_should_produce_positive_result(self):
    result = ornstein_uhlenbeck(x=1, mu=0, theta=0.15, sigma=0.2)

    # Assert using 95 condifidence interval.
    self.assertGreaterEqual(result, -0.542)
    self.assertLessEqual(result, 0.242)


if __name__ == "__main__":
  unittest.main()
