import pandas as pd
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns

# Load WM summary data
df = pd.read_csv('wm_parameter_stability_summary.csv')

# Define parameter columns across 11 trials
epsilon_cols = [f'epsilon_t{i}' for i in range(1, 12)]
capacity_cols = [f'capacity_t{i}' for i in range(1, 12)]
w0_cols = [f'w0_t{i}' for i in range(1, 12)]
beta_wm_cols = [f'beta_wm_t{i}' for i in range(1, 12)]

# Melt each to long format
def melt_param(df, cols, name):
    long_df = df.melt(id_vars='subno', value_vars=cols, var_name='trial', value_name=name)
    long_df['trial'] = long_df['trial'].str.extract('(\d+)').astype(int)
    return long_df

epsilon_long = melt_param(df, epsilon_cols, 'epsilon')
capacity_long = melt_param(df, capacity_cols, 'capacity')
w0_long = melt_param(df, w0_cols, 'w0')
beta_wm_long = melt_param(df, beta_wm_cols, 'beta_wm')

# Compute our means and stds
means_stds = {
    'epsilon': (epsilon_long['epsilon'].mean(), epsilon_long['epsilon'].std()),
    'capacity': (capacity_long['capacity'].mean(), capacity_long['capacity'].std()),
    'w0': (w0_long['w0'].mean(), w0_long['w0'].std()),
    'beta_wm': (beta_wm_long['beta_wm'].mean(), beta_wm_long['beta_wm'].std())
}

# Collins WM reported values
collins = {
    'epsilon': (0.1, 0.005),
    'capacity': (5.4, 0.8),
    'w0': (0.95, 0.005),
    'beta_wm': (12.0, 1.3)
}

# Set style
sns.set_style("whitegrid")

# Plot function
def plot_param(data_long, param, color, collins_color):
    mean_val, std_val = means_stds[param]
    collins_val, collins_std = collins[param]

    plt.figure(figsize=(10, 5))
    sns.boxplot(x='trial', y=param, data=data_long, color=color)
    plt.title(f'{param} Distribution Across 11 Trials (WM Model)')

    # Collins band
    plt.axhspan(collins_val - collins_std, collins_val + collins_std,
                color=collins_color, alpha=0.15, label=f'Collins {param} ±1 SD')
    plt.axhline(collins_val, color=collins_color, linestyle='-', linewidth=1.5)

    # Our mean ± std line
    plt.axhline(mean_val, color='black', linestyle='--', linewidth=1.5, label=f'Our mean {param}')
    plt.text(10.6, mean_val + std_val * 0.2, f'{mean_val:.2f}±{std_val:.2f}', color='black')
    plt.text(10.6, collins_val + collins_std * 0.2, f'{collins_val:.2f}±{collins_std:.2f}', color=collins_color)

    plt.ylabel(param)
    plt.legend()
    plt.show()

# Generate plots
plot_param(epsilon_long, 'epsilon', 'skyblue', 'green')
plot_param(capacity_long, 'capacity', 'lightcoral', 'orange')
plot_param(w0_long, 'w0', 'lightgray', 'purple')
plot_param(beta_wm_long, 'beta_wm', 'khaki', 'darkred')

