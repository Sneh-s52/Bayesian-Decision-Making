import numpy as np
import matplotlib.pyplot as plt
from scipy.special import softmax

# ==== RLWM parameter estimates from your Stan fit ====
alpha_rl = 0.868316
beta_rl = 6.090153
beta_wm = 4.578272
forget = 0.006104
w0 = 0.224626
epsilon = 0.027270
stick = 1.579407
C = 3  # assumed capacity (your model samples this; adjust if known)

# ==== Simulation settings ====
n_trials = 10
n_actions = 3
set_sizes = [2, 3, 4, 5, 6]

# ==== Generate learning curves ====
learning_curves = {}

# Reproducibility
np.random.seed(42)

for set_size in set_sizes:
    Q = np.ones((1, n_actions)) / n_actions
    WM = np.ones((1, n_actions)) / n_actions
    prev_choice = np.zeros(n_actions)
    
    performance = []
    p_in_wm = min(1.0, C / set_size)
    w = w0 * p_in_wm  # Adjusted WM weight based on set size

    for t in range(n_trials):
        # Compute policies
        Q_policy = softmax(beta_rl * (Q[0] + stick * prev_choice))
        WM_policy = softmax(beta_wm * (WM[0] + stick * prev_choice))

        # Combine with lapse
        policy = w * ((1 - epsilon) * WM_policy + epsilon / n_actions) + \
                 (1 - w) * ((1 - epsilon) * Q_policy + epsilon / n_actions)

        # Sample correct action (assume action 0 is always correct)
        correct_action = 0
        action = np.random.choice(n_actions, p=policy)
        correct = int(action == correct_action)
        performance.append(correct)

        # Simulated binary reward
        reward = 1 if action == correct_action else 0

        # RL update
        Q[0, action] += alpha_rl * (reward - Q[0, action])

        # WM update with decay
        WM += forget * (1 / n_actions - WM)
        WM[0, action] += (reward - WM[0, action])

        # Update previous choice
        prev_choice = np.zeros(n_actions)
        prev_choice[action] = 1

    # Smooth performance with moving average (optional)
    learning_curves[set_size] = np.array(performance)

# ==== Plotting ====
colors = {
    2: '#0C90C1',  # blue
    3: '#8FBE3F',  # green
    4: '#FFC328',  # yellow
    5: '#F27127',  # orange
    6: '#D8383A'   # red
}

markers = {
    1: 'o',
    2: 's',
    3: 'D',
    4: '^',
    5: 'v',
    6: 'P'
}

plt.figure(figsize=(5, 4))
trials = np.arange(1, n_trials + 1)

for set_size in set_sizes:
    curve = learning_curves[set_size]
    plt.plot(
        trials,
        curve,
        label=f'{set_size}',
        color=colors[set_size],
        marker=markers.get(set_size, 'o'),
        markersize=5,
        linewidth=1.5
    )

plt.title('RLWM Model Learning Curves', fontsize=14)
plt.ylim(0.2, 1.0)
plt.xlim(0.5, n_trials + 0.5)
plt.xlabel('Trials per stimulus', fontsize=12)
plt.ylabel('Proportion correct', fontsize=12)
plt.xticks(np.arange(2, n_trials + 1, 2), fontsize=10)
plt.yticks(np.arange(0.2, 1.1, 0.2), fontsize=10)
plt.legend(loc='lower right', fontsize=8, title='Set size')
plt.tight_layout()
plt.show()
