from gym_game_controller import MyGameEnv
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import BaseCallback
import numpy as np
import matplotlib.pyplot as plt

from stable_baselines3.common import results_plotter

    
env = MyGameEnv(20)  # No need to wrap the environment
model = DQN('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=5000000)
model.save("dqn_mlp")
