import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the summary file
df = pd.read_csv('wm_parameter_stability_summary.csv')

# Set subject number as index
df.set_index('subno', inplace=True)

# Plot heatmaps for each parameter
parameters = ['epsilon', 'capacity', 'w0', 'beta_wm']

for param in parameters:
    # Extract only the trial-wise columns for this parameter
    param_cols = [col for col in df.columns if col.startswith(param)]
    heatmap_data = df[param_cols].T  # Transpose so trials are rows, subjects are columns

    # Create the heatmap
    plt.figure(figsize=(16, 4))  # Wider to accommodate many subjects
    sns.heatmap(heatmap_data, cmap='viridis', cbar_kws={'label': param}, xticklabels=True, yticklabels=True)
    plt.title(f"Heatmap of {param} Across Subjects and Trials")
    plt.xlabel("Subject")
    plt.ylabel("Trial")
    plt.tight_layout()
    plt.show()

