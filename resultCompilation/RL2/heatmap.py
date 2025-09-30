import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the summary file
df = pd.read_csv('alpha_beta_stability_summary.csv')

# Set subject number as index
df.set_index('subno', inplace=True)

# List of RL2 parameters
parameters = ['alpha', 'beta']

for param in parameters:
    # Get all columns related to the current parameter
    param_cols = [col for col in df.columns if col.startswith(param)]
    
    # Transpose for heatmap: trials as rows, subjects as columns
    heatmap_data = df[param_cols].T
    
    # Plot heatmap
    plt.figure(figsize=(16, 4))  # Adjust width for many subjects
    sns.heatmap(heatmap_data, cmap='magma', cbar_kws={'label': param}, xticklabels=True, yticklabels=True)
    plt.title(f"Heatmap of {param} Across Subjects and Trials")
    plt.xlabel("Subject")
    plt.ylabel("Trial")
    plt.tight_layout()
    plt.show()

