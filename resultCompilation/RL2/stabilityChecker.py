import pandas as pd
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('alpha_beta_stability_summary.csv')

# Generate trial column names
alpha_cols = [f'alpha_t{i}' for i in range(1, 13)]
beta_cols = [f'beta_t{i}' for i in range(1, 13)]

# Melt to long format
alpha_long = df.melt(id_vars='subno', value_vars=alpha_cols, var_name='trial', value_name='alpha')
beta_long = df.melt(id_vars='subno', value_vars=beta_cols, var_name='trial', value_name='beta')

# Extract trial numbers
alpha_long['trial'] = alpha_long['trial'].str.extract('(\d+)').astype(int)
beta_long['trial'] = beta_long['trial'].str.extract('(\d+)').astype(int)

# Compute mean and std for Our data
alpha_mean = alpha_long['alpha'].mean()
alpha_std = alpha_long['alpha'].std()

beta_mean = beta_long['beta'].mean()
beta_std = beta_long['beta'].std()

# Collins values (RL2)
collins_alpha = 0.38
collins_alpha_std = 0.02
collins_beta = 7.1
collins_beta_std = 0.6

# Set global seaborn style
sns.set_style("whitegrid")

# --- Alpha Plot ---
plt.figure(figsize=(10, 5))
sns.boxplot(x='trial', y='alpha', data=alpha_long, color='skyblue')
plt.title('RL2 Alpha Distribution Across 12 Trials')

# Collins mean ± std shaded band
plt.axhspan(collins_alpha - collins_alpha_std, collins_alpha + collins_alpha_std,
            color='green', alpha=0.15, label='Collins α ±1 SD')
plt.axhline(collins_alpha, color='green', linestyle='-', linewidth=1.5)

# Our mean ± std line
plt.axhline(alpha_mean, color='blue', linestyle='--', linewidth=1.5, label='Our mean α')
plt.text(11.3, alpha_mean + 0.01, f'{alpha_mean:.2f}±{alpha_std:.2f}', color='blue')
plt.text(11.3, collins_alpha + 0.01, f'{collins_alpha:.2f}±{collins_alpha_std:.2f}', color='green')

plt.ylabel('Alpha')
plt.legend()
plt.show()

# --- Beta Plot ---
plt.figure(figsize=(10, 5))
sns.boxplot(x='trial', y='beta', data=beta_long, color='lightcoral')
plt.title('RL2 Beta Distribution Across 12 Trials')

# Collins mean ± std shaded band
plt.axhspan(collins_beta - collins_beta_std, collins_beta + collins_beta_std,
            color='darkorange', alpha=0.15, label='Collins β ±1 SD')
plt.axhline(collins_beta, color='darkorange', linestyle='-', linewidth=1.5)

# Our mean ± std line
plt.axhline(beta_mean, color='steelblue', linestyle='--', linewidth=1.5, label='Our mean β')
plt.text(11.3, beta_mean + 0.5, f'{beta_mean:.2f}±{beta_std:.2f}', color='steelblue')
plt.text(11.3, collins_beta + 0.5, f'{collins_beta:.2f}±{collins_beta_std:.2f}', color='darkorange')

plt.ylabel('Beta')
plt.legend()
plt.show()

