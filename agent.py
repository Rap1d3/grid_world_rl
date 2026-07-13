

import random
from environment import Action, REWARDS

class QAgent:
    def __init__(self , alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.995,  epsilon_min=0.01):
        self.alpha = alpha
        self.gamma = gamma 
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.q_table = {}
    
    def get_q(self , state, action):
        return self.q_table.get((state, action),0)

    def choose_action(self, state):
        rint = random.random()
        actions = list(Action)
        if rint < self.epsilon:
            return random.choice(actions)
        else:
            return max(actions , key = lambda action: self.get_q(state, action))
    
    def learn(self, state, action, reward , next_state, done):
        actions = list(Action)
        if done:
            best_next_q = 0
        else:
            best_next_q = max(self.get_q(next_state , a) for a in actions)
        current_q = self.get_q(state, action)
        self.q_table[(state, action)] = current_q + self.alpha*(reward + self.gamma*best_next_q - current_q)

