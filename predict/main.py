import pandas as pd
import os

# Folder path
input_folder = r"D:/NYU_research/big_data/raw/raw/states"
output_file = r"D:/NYU_research/big_data/raw/raw/states_filtered/all_filtered_data.txt"

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Create an empty list to accumulate all filtered data
all_data = []

# Iterate over all txt files
for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(input_folder, filename)

        # Read individual file
        try:
            df = pd.read_csv(file_path, sep='\t', engine='python')
            df.columns = df.columns.str.strip()  # Remove whitespace from column names
        except Exception as e:
            print(f"Failed to read {filename}: {e}")
            continue

        # Check that 'series_id' column exists
        if 'series_id' not in df.columns:
            print(f"Skipping {filename} (no 'series_id' column)")
            continue

        # Filter rows where series_id ends with '003' (after stripping)
        filtered_df = df[df['series_id'].astype(str).str.strip().str.endswith('003')]

        if filtered_df.empty:
            print(f"No valid data in {filename}, skipping.")
            continue

        # Extract state name from filename, e.g., la.data.7.Alabama.txt -> Alabama
        state_name = filename.split('.')[-2]
        filtered_df['state_name'] = state_name

        # Add filtered data to the list
        all_data.append(filtered_df)

        print(f"Filtered data from {filename}, {len(filtered_df)} rows, state={state_name}")

# After processing all files, concatenate into a single DataFrame
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)

    # Save to a single output txt file
    final_df.to_csv(output_file, sep='\t', index=False)

    print(f"All filtered data saved to {output_file}")
else:
    print("No data matched filter conditions.")
