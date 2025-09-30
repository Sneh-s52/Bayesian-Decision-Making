import pandas as pd
import glob

# List of WM filenames
filenames = sorted(glob.glob('trials/wm_results_[1-9].csv') +
                   glob.glob('trials/wm_results_1[0-1].csv'))

# Create empty dataframe to hold final results
final_df = pd.DataFrame()

# Loop through each file
for i, file in enumerate(filenames, start=1):
    # Read the CSV
    df = pd.read_csv(file, sep=',')
    
    # Group by subject and calculate mean of WM parameters
    means = df.groupby('subno')[['epsilon', 'capacity', 'w0', 'beta_wm']].mean().reset_index()
    
    # Rename columns to reflect trial number
    means.rename(columns={
        'epsilon': f'epsilon_t{i}',
        'capacity': f'capacity_t{i}',
        'w0': f'w0_t{i}',
        'beta_wm': f'beta_wm_t{i}'
    }, inplace=True)
    
    # Merge with final_df
    if final_df.empty:
        final_df = means
    else:
        final_df = pd.merge(final_df, means, on='subno', how='outer')

# Sort by subject number
final_df.sort_values(by='subno', inplace=True)

# Save final table
final_df.to_csv('wm_parameter_stability_summary.csv', index=False)

print("✅ Summary table saved as 'wm_parameter_stability_summary.csv'")

