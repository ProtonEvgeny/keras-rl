import random

import numpy as np
from numpy.testing import assert_allclose

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam
from rl.agents import DQNAgent, CEMAgent, SARSAAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory, EpisodeParameterMemory
from utils.gym.envs import TwoRoundDeterministicRewardEnv


def test_dqn():
    env = TwoRoundDeterministicRewardEnv()
    np.random.seed(123)
    random.seed(123)
    nb_actions = env.action_space.n

    # Next, we build a very simple model.
    model = Sequential()
    model.add(Dense(16, input_shape=(1,)))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions))
    model.add(Activation('linear'))

    memory = SequentialMemory(limit=1000, window_length=1)
    policy = EpsGreedyQPolicy(eps=.1)
    dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=50,
                   target_model_update=1e-1, policy=policy, enable_double_dqn=False)
    dqn.compile(Adam(lr=1e-3))

    dqn.fit(env, nb_steps=2000, verbose=0)
    policy.eps = 0.
    h = dqn.test(env, nb_episodes=20)
    assert_allclose(np.mean(h.history['episode_reward']), 3.)


def test_double_dqn():
    env = TwoRoundDeterministicRewardEnv()
    np.random.seed(123)
    random.seed(123)
    nb_actions = env.action_space.n

    # Next, we build a very simple model.
    model = Sequential()
    model.add(Dense(16, input_shape=(1,)))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions))
    model.add(Activation('linear'))

    memory = SequentialMemory(limit=1000, window_length=1)
    policy = EpsGreedyQPolicy(eps=.1)
    dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=50,
                   target_model_update=1e-1, policy=policy, enable_double_dqn=True)
    dqn.compile(Adam(lr=1e-3))

    dqn.fit(env, nb_steps=2000, verbose=0)
    policy.eps = 0.
    h = dqn.test(env, nb_episodes=20)
    assert_allclose(np.mean(h.history['episode_reward']), 3.)


def test_cem():
    env = TwoRoundDeterministicRewardEnv()
    np.random.seed(123)
    random.seed(123)
    nb_actions = env.action_space.n

    # Next, we build a very simple model.
    model = Sequential()
    model.add(Dense(16, input_shape=(1,)))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions))
    model.add(Activation('linear'))

    memory = EpisodeParameterMemory(limit=1000, window_length=1)
    dqn = CEMAgent(model=model, nb_actions=nb_actions, memory=memory)
    dqn.compile()

    dqn.fit(env, nb_steps=2000, verbose=1)
    h = dqn.test(env, nb_episodes=20)
    assert_allclose(np.mean(h.history['episode_reward']), 3.)


def test_duel_dqn():
    env = TwoRoundDeterministicRewardEnv()
    np.random.seed(123)
    random.seed(123)
    nb_actions = env.action_space.n

    # Next, we build a very simple model.
    model = Sequential()
    model.add(Dense(16, input_shape=(1,)))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions, activation='linear'))

    memory = SequentialMemory(limit=1000, window_length=1)
    policy = EpsGreedyQPolicy(eps=.1)
    dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=50,
                   target_model_update=1e-1, policy=policy, enable_double_dqn=False, enable_dueling_network=True)
    dqn.compile(Adam(lr=1e-3))

    dqn.fit(env, nb_steps=2000, verbose=0)
    policy.eps = 0.
    h = dqn.test(env, nb_episodes=20)
    assert_allclose(np.mean(h.history['episode_reward']), 3.)


def test_sarsa():
    env = TwoRoundDeterministicRewardEnv()
    np.random.seed(123)
    random.seed(123)
    nb_actions = env.action_space.n

    # Next, we build a very simple model.
    model = Sequential()
    model.add(Dense(16, input_shape=(1,)))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions, activation='linear'))

    policy = EpsGreedyQPolicy(eps=.1)
    sarsa = SARSAAgent(model=model, nb_actions=nb_actions, nb_steps_warmup=50, policy=policy)
    sarsa.compile(Adam(lr=1e-3))

    sarsa.fit(env, nb_steps=20000, verbose=0)
    policy.eps = 0.
    h = sarsa.test(env, nb_episodes=20)
    assert_allclose(np.mean(h.history['episode_reward']), 3.)
