"""The critic network, also known as the value network.

Based on the paper: Continuous control with deep reinforcement learning (2015) by Lillicrap.
"""
from keras.layers import Dense, Input, Add
from keras.models import Model
from keras.optimizers import Adam
from keras.initializers import RandomUniform
import keras.backend as K
import tensorflow as tf

HIDDEN_LAYER_1_NEURON_SIZE = 400
HIDDEN_LAYER_2_NEURON_SIZE = 300


class CriticNetwork(object):
  """The critic network, also known as the value network.

  The critic network produces signals to criticize the actions made by the actor network. In
  addition, the critic network takes both the state and the action as inputs. According to the
  original paper, the action was not included until the 2nd hidden layer of Q-network.

  Attributes:
    model: The neural network model of value network.
    target_model: The target neural network model of value network.
  """

  def __init__(self, session, state_size, action_size, tau=0.001, learning_rate=0.001):
    """Constructs an CriticNetwork.

    Args:
      session: Tensorflow session, usually obtained by tf.Session().
      state_size: The number of states for a given environment.
      action_size: The number of real value actions for a given environment.
      tau: The rate of soft target network weights update.
      learning_rate: The learning rate for the optimizer of the neural network.

    Returns:
      An instance of CriticNetwork.
    """
    self._session = session
    self._tau = tau

    K.set_session(session)

    self.model, self._action, self._state = \
        self._create_critic_network(state_size, action_size, learning_rate)
    self.target_model, unused_target_action, unused_target_state = \
        self._create_critic_network(state_size, action_size, learning_rate)

    self._action_gradient = tf.gradients(self.model.output, self._action)

  def action_gradient(self, state, action):
    """Returns the gradients for policy update for actor network.

    Args:
      state: The state to be used for mini-batch gradient updates.
      action: The action taken by actor network.

    Returns:
      The action gradient to be used to update actor network.
    """
    feed_dict = {self._state: state, self._action: action}
    return self._session.run(self._action_gradient, feed_dict=feed_dict)[0]

  def target_train(self):
    """Trains the target value neural network.

    The target neural network weight is updated using "soft" target updates, rather than directly
    copying the weights (which is done in original DQN). Only tau ratio of current value neural
    network weight is copied to current target value neural network. The formula is:

      value_target_nn_weights = tau * value_nn_weights + (1 - tau) * value_target_nn_weights

    This means that the target values are constrained to change slowly, greatly improving the
    stability of learning.
    """
    critic_weights = self.model.get_weights()
    critic_target_weights = self.target_model.get_weights()
    for i, critic_weight in enumerate(critic_weights):
      critic_target_weights[i] = \
          self._tau * critic_weight + (1 - self._tau) * critic_target_weights[i]
    self.target_model.set_weights(critic_target_weights)

  def _create_critic_network(self, state_size, action_size, learning_rate):
    """Creates a neural network for value network.

    According to the original paper, the value network contains 400 neurons in the first hidden
    layer and 300 neurons in the second hidden layer, with ReLU activation function. The action is
    not included until the second layer of the neural network.

    Args:
      state_size: The number of states for a given environment.
      action_size: The number of real value actions for a given environment.
      output_layer_activation: The activation function of output layer. Possible values would be
        'sigmoid' or 'relu'.

    Returns:
      The created neural network model and the placeholder input state.
    """
    state = Input(shape=[state_size])
    action = Input(shape=[action_size])

    # Only include state in the first hidden layer
    hidden_layer_1 = Dense(
        HIDDEN_LAYER_1_NEURON_SIZE,
        activation='relu',
        kernel_initializer='he_uniform',
        bias_initializer='he_uniform')(state)

    # Technically there are only 2 hidden layer in critic network. However the layer_2 in the
    # following codes are intermidiate layer before layer_3.
    hidden_layer_2_state = Dense(
        HIDDEN_LAYER_2_NEURON_SIZE,
        activation='linear',
        kernel_initializer='he_uniform',
        bias_initializer='he_uniform')(hidden_layer_1)
    hidden_layer_2_action = Dense(
        HIDDEN_LAYER_2_NEURON_SIZE,
        activation='linear',
        kernel_initializer='he_uniform',
        bias_initializer='he_uniform')(action)
    hidden_layer_2 = Add()([hidden_layer_2_state, hidden_layer_2_action])

    hidden_layer_3 = Dense(
        HIDDEN_LAYER_2_NEURON_SIZE,
        activation='relu',
        kernel_initializer='he_uniform',
        bias_initializer='he_uniform')(hidden_layer_2)

    output_layer_initializer = RandomUniform(minval=1e-4, maxval=1e-4, seed=None)
    output_layer = Dense(
        action_size,
        activation='linear',
        kernel_initializer=output_layer_initializer,
        bias_initializer=output_layer_initializer)(hidden_layer_3)

    model = Model(inputs=[state, action], outputs=output_layer)
    adam = Adam(lr=learning_rate)
    model.compile(loss='mse', optimizer=adam)
    return model, action, state
