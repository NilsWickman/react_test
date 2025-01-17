import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque
from model import FIR_model
from environment import env

# Hyperparameters
gamma = 0.99  # Discount factor
epsilon = 1.0  # Exploration rate
epsilon_decay = 0.995
epsilon_min = 0.1
batch_size = 64
learning_rate = 1e-3

# Initialize components
model = FIR_model()
target_model = FIR_model()  # For stability in DQN
target_model.load_state_dict(model.state_dict())
target_model.eval()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)
replay_buffer = deque(maxlen=10000)

env = env()

def select_action(state, epsilon):
    if random.random() < epsilon:
        return random.randint(0, 6)  # Random action
    with torch.no_grad():
        q_values = model(torch.tensor(state, dtype=torch.float32).unsqueeze(0))
        return torch.argmax(q_values).item()

def train_step():
    if len(replay_buffer) < batch_size:
        return

    # Sample a batch
    batch = random.sample(replay_buffer, batch_size)
    states, actions, rewards, next_states, dones = zip(*batch)

    # Convert to tensors
    states = torch.tensor(states, dtype=torch.float32)
    actions = torch.tensor(actions, dtype=torch.long)
    rewards = torch.tensor(rewards, dtype=torch.float32)
    next_states = torch.tensor(next_states, dtype=torch.float32)
    dones = torch.tensor(dones, dtype=torch.float32)

    # Compute Q-values
    q_values = model(states)
    q_values = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)

    # Compute target Q-values
    with torch.no_grad():
        next_q_values = target_model(next_states).max(1)[0]
        targets = rewards + gamma * next_q_values * (1 - dones)

    # Compute loss and optimize
    loss = nn.MSELoss()(q_values, targets)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

for episode in range(1000):  # Number of episodes
    state = env.reset()  # Initialize environment
    done = False
    total_reward = 0

    while not done:
        action = select_action(state, epsilon)
        print(action)
        next_state, reward, done = env.step(action)

        # Store in replay buffer
        replay_buffer.append((state, action, reward, next_state, done))

        state = next_state
        total_reward += reward

        train_step()

    # Update epsilon
    epsilon = max(epsilon * epsilon_decay, epsilon_min)

    # Update target model periodically
    if episode % 10 == 0:
        target_model.load_state_dict(model.state_dict())

    print(f"Episode {episode}, Total Reward: {total_reward}")

