"""The Deep Deterministic Policy Gradient (DDPG) agent.

Based on the paper: Continuous control with deep reinforcement learning (2015) by Lillicrap.
"""
import tensorflow as tf
from keras import backend as K
import numpy as np

from bunnieddpg.critic_net import CriticNetwork
from bunnieddpg.actor_net import ActorNetwork
from bunnieddpg.replay_buffer import ReplayBuffer
from bunnieddpg.ornstein_uhlenbeck import ornstein_uhlenbeck


class DeepDeterministicPolicyGradientAgent(object):
  """The DDPG agent.

  This agent adapts the idea from Deep Q-Learning to continuous action domain. It contains two
  neural network internally, i.e. the actor network and the critic network. For more information,
  about the actor network and critic network, please refer to ActorNetwork and CriticNetwork class.

  Attributes:
    session: Tensorflow session, usually obtained by tf.Session().
    epsilon: The rate of randomness of the predicted continuous action.
    replay_buffer: The replay buffer that is used to save previously seen experience, and sample
      experience randomly to replay the experience to train the neural networks using mini-batch
      training.
  """

  def __init__(self,
               state_size,
               action_size,
               batch_size=64,
               buffer_size=1000000,
               reward_discount_rate=0.99,
               epsilon=1,
               epsilon_decay_rate=0.01,
               ou_mean=0,
               ou_theta=0.15,
               ou_sd=0.2):
    """Initializes a DDPG agent.

    Args:
      state_size: The number of states for a given environment.
      action_size: The number of real value actions for a given environment.
      batch_size: The number of experience/examples per mini-batch of training.
      buffer_size: The maximum number of experience/examples that are stored in the replay_buffer.
      reward_discount_rate: The reward discount factor of Q-Learning.
      epsilon: The initial probability of taking random action.
      epsilon_decay_rate: The decay rate of epsilon. This will be used to reduce epsilon value
        everytime the predict() method is called.
      ou_mean: The Ornstein Uhlenbeck process mean.
      ou_theta: The Ornstein Uhlenbeck process theta.
      ou_sd: The Ornstein Uhlenbeck process standard deviation.

    Returns:
      An instance of DeepDeterministicPolicyGradientAgent.
    """
    self._state_size = state_size
    self._action_size = action_size
    self._batch_size = batch_size
    self._reward_discount_rate = reward_discount_rate
    self._epsilon_decay_rate = epsilon_decay_rate
    self._ou_mean = ou_mean
    self._ou_theta = ou_theta
    self._ou_sd = ou_sd

    self.epsilon = epsilon

    self.session = tf.Session()
    K.set_session(self.session)

    self._actor_network = ActorNetwork(self.session, state_size, action_size)
    self._critic_network = CriticNetwork(self.session, state_size, action_size)
    self.replay_buffer = ReplayBuffer(buffer_size)

    tf.global_variables_initializer()

  def load_weights(self, actor_weights_file_name, critic_weights_file_name):
    """Loads the weights of actor neural network and critic neural network.

    Args:
      actor_weights_file_name: The name of HDF5 file for weights of actor neural network.
      critic_weights_file_name: The name of HDF5 file for weights of critic neural network.

    Raises:
      OSError: An error occurred accessing the files with given names.
    """
    self._actor_network.model.load_weights(actor_weights_file_name)
    self._actor_network.target_model.load_weights(actor_weights_file_name)
    self._critic_network.model.load_weights(critic_weights_file_name)
    self._critic_network.target_model.load_weights(critic_weights_file_name)

  def save_weights(self, actor_weights_file_name, critic_weights_file_name):
    """Saves the weights of critic neural network and critic neural network.

    Args:
      actor_weights_file_name: The name of HDF5 file for weights of actor neural network.
      critic_weights_file_name: The name of HDF5 file for weights of critic neural network.

    Raises:
      OSError: An error accurred accessing the files with the given names.
    """
    self._actor_network.model.save_weights(actor_weights_file_name, overwrite=True)
    self._critic_network.model.save_weights(critic_weights_file_name, overwrite=True)

  def predict(self, state):
    """Predicts the real value actions to be taken based on current state and epsilon.

    Args:
      state: The state of the environment when the action is taken. The state should be a numpy
          array with size of [1, state_size].

    Returns:
      An array of actions to be taken by the agent. The size of the array is [1, action_size]
    """
    state = state.reshape(1, self._state_size)
    predicted_action = self._actor_network.model.predict(state)
    action_noise = self.epsilon * ornstein_uhlenbeck(predicted_action, self._ou_mean,
                                                     self._ou_theta, self._ou_sd)

    assert predicted_action.shape[0] == 1
    assert predicted_action.shape[1] == self._action_size
    assert action_noise.shape[0] == 1
    assert action_noise.shape[1] == self._action_size

    action_with_noise = predicted_action + action_noise

    # Flatten the action shape.
    action_with_noise = action_with_noise[0]

    # Update the randomness of next prediction
    self.epsilon = max(self.epsilon - self._epsilon_decay_rate, 0)

    return action_with_noise

  def add_experience(self, state, action, reward, new_state, done):
    """Adds an experience to the replay_buffer.

    Args:
      state: The state of the environment before an action is performed.
      action: The action that has been taken in the state.
      reward: The reward obtained from the environment after the action is performed.
      new_state: The new state of the environment after the action is performed.
      done: Whether the game is finished.
    """
    self.replay_buffer.add_experience(state, action, reward, new_state, done)

  def replay_experience(self):
    """Perform batch update for actor neural network and critic neural network.

    A number of batch_size experience are sampled randomly from the replay_buffer, and are used to
    perform batch update for both neural networks.
    """
    batch = self.replay_buffer.random_experience(self._batch_size)

    # Flatten the randomly sampled experience to multiple lists.
    states = np.asarray([e[0] for e in batch])
    actions = np.asarray([e[1] for e in batch])
    rewards = np.asarray([e[2] for e in batch])
    new_states = np.asarray([e[3] for e in batch])
    dones = np.asarray([e[4] for e in batch])
    y_t = np.asarray([e[1] for e in batch])

    predicted_actions_for_new_states = self._actor_network.target_model.predict(new_states)
    target_q_values = \
        self._critic_network.target_model.predict([new_states, predicted_actions_for_new_states])

    for k in range(len(batch)):
      if dones[k]:
        y_t[k] = rewards[k]
      else:
        y_t[k] = rewards[k] + self._reward_discount_rate * target_q_values[k]

    unused_loss = self._critic_network.model.train_on_batch([states, actions], y_t)
    a_for_grad = self._actor_network.model.predict(states)
    grads = self._critic_network.action_gradient(states, a_for_grad)
    self._actor_network.train(states, grads)
    self._actor_network.target_train()
    self._critic_network.target_train()
