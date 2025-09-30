import pandas as pd
import glob

# List of filenames
filenames = sorted(glob.glob('trials/rl2_updated_results_[1-9].csv') + 
                   glob.glob('trials/rl2_updated_results_1[0-2].csv'))
# Create empty dataframe to hold final results
final_df = pd.DataFrame()

# Loop through each file
for i, file in enumerate(filenames, start=1):
    # Read the CSV
    df = pd.read_csv(file, sep=',')  # use sep=',' if comma-separated
    
    # Group by subject and calculate mean of alpha and beta
    means = df.groupby('subno')[['alpha', 'beta']].mean().reset_index()
    
    # Rename columns to reflect trial number
    means.rename(columns={'alpha': f'alpha_t{i}', 'beta': f'beta_t{i}'}, inplace=True)
    
    # Merge with final_df
    if final_df.empty:
        final_df = means
    else:
        final_df = pd.merge(final_df, means, on='subno', how='outer')

# Sort by subject number
final_df.sort_values(by='subno', inplace=True)

# Save final table
final_df.to_csv('alpha_beta_stability_summary.csv', index=False)

print("Summary table saved as 'alpha_beta_stability_summary.csv'")
