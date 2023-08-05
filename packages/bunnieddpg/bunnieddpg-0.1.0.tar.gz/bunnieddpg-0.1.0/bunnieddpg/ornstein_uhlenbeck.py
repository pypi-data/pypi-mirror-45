"""Defines function for Ornstein Uhlenbeck process.

Taken from https://github.com/openai/baselines/blob/master/baselines/ddpg/noise.py, which is
based on http://math.stackexchange.com/questions/1287634/implementing-ornstein-uhlenbeck-in-matlab
"""
import numpy as np


def ornstein_uhlenbeck(x, mu, theta, sigma):
  """The Ornstein Uhlenbeck function."""
  return theta * (mu - x) + sigma * np.random.randn(1)
