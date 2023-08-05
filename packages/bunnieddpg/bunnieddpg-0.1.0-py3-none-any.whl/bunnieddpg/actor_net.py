"""The actor network, also known as the policy network.

Based on the paper: Continuous control with deep reinforcement learning (2015) by Lillicrap.
"""
from keras.layers import Dense, Input
from keras.models import Model
from keras.initializers import RandomUniform
import tensorflow as tf

HIDDEN_LAYER_1_NEURON_SIZE = 400
HIDDEN_LAYER_2_NEURON_SIZE = 300


class ActorNetwork(object):
  """The actor network, also known as the policy network.

  It is used to compute the estimation the policy function. The policy function is defined as the
  probability to take an action a, given the states of environments s, and some weights theta. By
  having the estimation of policy function, this network is used to predict the greedy action based
  on current states.

  Attributes:
    model: The neural network model of actor network.
    target_model: The target neural network model of actor network.
  """

  def __init__(self, session, state_size, action_size, tau=0.001, learning_rate=0.0001):
    """Constructs an ActorNetwork.

    Args:
      session: Tensorflow session, usually obtained by tf.Session().
      state_size: The number of states for a given environment.
      action_size: The number of real value actions for a given environment.
      tau: The rate of soft target network weights update.
      learning_rate: The learning rate for the optimizer of the neural network.

    Returns:
      An instance of ActorNetwork.
    """
    self._session = session
    self._tau = tau

    self.model, self._state = self._create_actor_network(state_size, action_size)
    self.target_model, unused_target_state = self._create_actor_network(state_size, action_size)

    self._action_gradient = tf.placeholder(tf.float32, [None, action_size])
    params_gradient = \
        tf.gradients(self.model.output, self.model.trainable_weights, -self._action_gradient)

    grads = zip(params_gradient, self.model.trainable_weights)
    self._optimize = tf.train.AdamOptimizer(learning_rate).apply_gradients(grads)

  def train(self, state, action_gradient):
    """Trains the actor neural network.

    Args:
      state: The state to be used for mini-batch gradient updates.
      action_gradient: The gradients for policy update given by the critic network.
    """
    feed_dict = {self._state: state, self._action_gradient: action_gradient}
    self._session.run(self._optimize, feed_dict=feed_dict)

  def target_train(self):
    """Trains the target actor neural network.

    The target neural network weight is updated using "soft" target updates, rather than directly
    copying the weights (which is done in original DQN). Only tau ratio of current actor neural
    network weight is copied to current target actor neural network. The formula is:

      actor_target_nn_weights = tau * actor_nn_weights + (1 - tau) * actor_target_nn_weights

    This means that the target values are constrained to change slowly, greatly improving the
    stability of learning.
    """
    actor_weights = self.model.get_weights()
    actor_target_weights = self.target_model.get_weights()

    for i, actor_weight in enumerate(actor_weights):
      actor_target_weights[i] = self._tau * actor_weight + (1 - self._tau) * actor_target_weights[i]

    self.target_model.set_weights(actor_target_weights)

  def _create_actor_network(self, state_size, action_size, output_layer_activation='sigmoid'):
    """Creates a neural network for actor network.

    According to the original paper, the actor network contains 400 neurons in the first hidden
    layer and 300 neurons in the second hidden layer, with ReLU activation function. The output
    layer is using tanh activation function in the original paper, and the output will eventually
    be scaled to [-output * factor, output * factor], so that the output realistically map to some
    controller signals.

    It is also possible to define the output activation function as sigmoid function, as described
    in: https://yanpanlau.github.io/2016/10/11/Torcs-Keras.html

    Args:
      state_size: The number of states for a given environment.
      action_size: The number of real value actions for a given environment.
      output_layer_activation: The activation function of output layer. Possible values would be
        'sigmoid' or 'tanh'.

    Returns:
      The created neural network model and the placeholder input state.
    """
    state = Input(shape=[state_size])
    hidden_layer_1 = Dense(
        HIDDEN_LAYER_1_NEURON_SIZE,
        activation='relu',
        kernel_initializer='he_uniform',
        bias_initializer='he_uniform')(state)
    hidden_layer_2 = Dense(
        HIDDEN_LAYER_2_NEURON_SIZE,
        activation='relu',
        kernel_initializer='he_uniform',
        bias_initializer='he_uniform')(hidden_layer_1)

    output_layer_initializer = RandomUniform(minval=1e-3, maxval=1e-3, seed=None)
    output_layer = Dense(
        action_size,
        activation=output_layer_activation,
        kernel_initializer=output_layer_initializer,
        bias_initializer=output_layer_initializer)(hidden_layer_2)
    model = Model(inputs=state, outputs=output_layer)
    return model, state
