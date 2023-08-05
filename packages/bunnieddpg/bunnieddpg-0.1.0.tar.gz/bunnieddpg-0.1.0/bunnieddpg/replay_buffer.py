""" Data structure for implementing experience replay.
"""
from collections import deque
import random


class ReplayBuffer(object):
  """The reply buffer saves all previously seen experience in a buffer.

  The experience in the buffer can be sampled randomly to be replayed to some neural networks. When
  the number of experience in the buffer is full, then old experience will be removed from the
  buffer before new experience is added to the buffer.
  """

  def __init__(self, buffer_size):
    self.buffer_size = buffer_size
    self.experience_size = 0
    self._buffer = deque()

  def random_experience(self, batch_size):
    """Returns randomly sampled experience from the buffer."""
    if self.experience_size < batch_size:
      return random.sample(self._buffer, self.experience_size)
    return random.sample(self._buffer, batch_size)

  def add_experience(self, state, action, reward, new_state, done):
    """Adds new experience to the buffer."""
    experience = (state, action, reward, new_state, done)
    if self.experience_size < self.buffer_size:
      self._buffer.append(experience)
      self.experience_size += 1
    else:
      self._buffer.popleft()
      self._buffer.append(experience)

  def clear_experience(self):
    """Clears all experience in the buffer."""
    self._buffer = deque()
    self.experience_size = 0
