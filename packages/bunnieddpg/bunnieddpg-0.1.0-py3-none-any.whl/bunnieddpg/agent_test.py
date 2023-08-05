import unittest

import numpy as np
import bunnieddpg.agent


class DeepDeterministicPolicyGradientAgentTest(unittest.TestCase):
  """Tests for DeepDeterministicPolicyGradientAgent."""

  def setUp(self):
    """Initializes a PowerTAC wholesale market DDPG agent.

    The DDPG agent is used to predict wholesale market enery limit price/MWh. When this test was
    written, the following states are provided to the agent on each timeslot:
    - Hour of day for current timeslot
    - Day of week for current timeslot
    - Hour of day for the timeslot to be predicted
    - Day of week for the timeslot to be predicted
    """
    self._wholesale_market_agent = bunnieddpg.agent.DeepDeterministicPolicyGradientAgent(
        state_size=4, action_size=1)

  def test_initialization_should_success(self):
    self.assertIsNotNone(self._wholesale_market_agent)

  def test_predict_with_zero_epsilon_should_take_positive_action(self):
    """Tests the predict function of DDPG using epsilon equals to zero.

    Epsilon is the probability of taking random action. When epsilon is equal to zero, no random
    action will be taken by the agent. Instead, the agent will make prediction using output from
    actor network. Since the default output layer of actor network is a sigmoid function, the output
    value must be between zero and one, exclusively.
    """
    state = _create_state(
        hour_of_day=1, day_of_week=2, hour_of_day_for_prediction=3, day_of_week_for_prediction=4)

    self._wholesale_market_agent.epsilon = 0
    action = self._wholesale_market_agent.predict(state)
    self.assertEqual(len(action), 1)
    self.assertGreater(action[0], 0)
    self.assertLess(action[0], 1)

  def test_predict_with_one_epsilon_should_take_random_action(self):
    """Tests the predict function of DDPG using epsilon equals to one.

    Epsilon is the probability of taking random action. When epsilon is equal to one, the agent will
    take random action. Theoretically, the action value can be any real number.
    """
    state = _create_state(
        hour_of_day=1, day_of_week=2, hour_of_day_for_prediction=3, day_of_week_for_prediction=4)

    self._wholesale_market_agent.epsilon = 1
    action = self._wholesale_market_agent.predict(state)
    self.assertEqual(len(action), 1)

  def test_replay_experience_should_success(self):
    for i in range(256):
      state = _create_state(
          hour_of_day=np.random.randint(24),
          day_of_week=np.random.randint(7),
          hour_of_day_for_prediction=np.random.randint(24),
          day_of_week_for_prediction=np.random.randint(7))
      new_state = _create_state(
          hour_of_day=np.random.randint(24),
          day_of_week=np.random.randint(7),
          hour_of_day_for_prediction=np.random.randint(24),
          day_of_week_for_prediction=np.random.randint(7))
      self._wholesale_market_agent.add_experience(
          state=state,
          action=np.random.uniform(1),
          reward=np.random.uniform(100),
          new_state=new_state,
          done=False)
    self._wholesale_market_agent.replay_experience()


def _create_state(hour_of_day, day_of_week, hour_of_day_for_prediction, day_of_week_for_prediction):
  return np.array(
      [hour_of_day, day_of_week, hour_of_day_for_prediction, day_of_week_for_prediction])


if __name__ == "__main__":
  unittest.main()
