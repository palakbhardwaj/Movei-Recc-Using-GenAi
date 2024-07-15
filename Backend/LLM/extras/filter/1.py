import pandas as pd

# Load the two CSV files into DataFrames
df1 = pd.read_csv('1.csv')
df2 = pd.read_csv('2.csv')

# Merge the two DataFrames based on the 'original_title' column
merged_df = df1.merge(df2[['original_title', 'poster_url']], on='original_title', how='left')

# Fill in missing 'poster_url' values in df1 with the corresponding values from df2
df1['poster_url'].fillna(merged_df['poster_url'], inplace=True)

# Drop rows with empty 'poster_url' in df1
df1 = df1.dropna(subset=['poster_url'])

# Save the updated DataFrame back to a CSV file
df1.to_csv('merged_1.csv', index=False)

print("Data merged and saved to merged_1.csv.")

