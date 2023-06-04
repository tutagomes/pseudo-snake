import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random
import numpy as np

class DQN(nn.Module):
    def __init__(self, input_space, action_space):
        super(DQN, self).__init__()
        self.action_space = action_space
        self.input_space = input_space
        self.memory = deque(maxlen=50000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995

        self.layers = nn.Sequential(
            nn.Linear(input_space, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, self.action_space)
        )
        self.optimizer = optim.Adam(self.parameters())

    def save_model(self, file_path):
        torch.save(self.state_dict(), file_path)

    def load_model(self, file_path):
        self.load_state_dict(torch.load(file_path))

    def forward(self, x):
        return self.layers(x)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space)
        state = torch.from_numpy(state).float().unsqueeze(0)
        act_values = self(state)
        return torch.argmax(act_values).item()

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            state = torch.from_numpy(state).float().unsqueeze(0)
            action = torch.tensor([action], dtype=torch.int64)
            reward = torch.tensor([reward]).float()
            next_state = torch.from_numpy(next_state).float().unsqueeze(0)
            done = torch.tensor([done]).float()
            
            if not done:
                target = (reward + self.gamma * torch.max(self(next_state)).item())
            else:
                target = reward
            current = self(state)[0][action]
            loss = torch.nn.functional.mse_loss(current, target)
            
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay
                
    def play(self, game):
        state = game.get_state()
        done = False
        while not done:
            action = self.act(state)
            _, done = game.step(action)
            state = game.get_state()