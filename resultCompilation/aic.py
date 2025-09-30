import matplotlib.pyplot as plt
import numpy as np

# Given data
models = ['RL2', 'WM', 'RLWM']
log_likelihoods = {
    'RL2': -152.5275,
    'WM': -131.880,
    'RLWM': -54.5381
}
aics = {
    'RL2': 309.055,
    'WM': 271.800,
    'RLWM': 117.076
}

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Relative increase in likelihood compared to RL2
relative_increase = []
for model in ['WM', 'RLWM']:
    increase = (log_likelihoods[model] - log_likelihoods['RL2']) / abs(log_likelihoods['RL2']) * 100
    relative_increase.append(increase)

ax1.bar(['WM', 'RLWM'], relative_increase, color='gray')
ax1.set_ylabel('Increase in likelihood relative to RL2 (%)')
ax1.set_title('Increase in likelihood\nrelative to simple RL2')

# Plot 2: AIC difference compared to RL2
aic_diff = []
for model in ['RL2', 'WM', 'RLWM']:
    diff = aics[model] - aics['RL2']
    aic_diff.append(diff)

ax2.bar(['RL2', 'WM', 'RLWM'], aic_diff, color='gray')
ax2.set_ylabel('AIC - AIC(RL2)')
ax2.set_title('AIC-AIC(RL2 Foraging)')

plt.tight_layout()
plt.show()
