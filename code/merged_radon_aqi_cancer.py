import pandas as pd
import os

# Define the directory where datasets are stored
TARGET_DIRECTORY = "/media/volume1"

# Define file paths
radon_file_path = os.path.join(TARGET_DIRECTORY, "cleaned_radon_zones.csv")
aqi_cancer_file_path = os.path.join(TARGET_DIRECTORY, "merged_aqi_cancer.csv")
output_file_path = os.path.join(TARGET_DIRECTORY, "final_merged_dataset.csv")

def merge_radon_aqi_cancer():
    """
    Merges the cleaned Radon dataset with the AQI-Cancer dataset.
    Expands the Radon data to match years in AQI-Cancer dataset.
    Prints the total number of rows, columns, column names, and first 10 rows.
    """
    if not os.path.exists(radon_file_path):
        print(f"Error: Radon file '{radon_file_path}' not found.")
        return None

    if not os.path.exists(aqi_cancer_file_path):
        print(f"Error: AQI-Cancer file '{aqi_cancer_file_path}' not found.")
        return None

    try:
        # Load datasets
        radon_df = pd.read_csv(radon_file_path)
        aqi_cancer_df = pd.read_csv(aqi_cancer_file_path)

        print("Datasets loaded successfully.")

        # Extract unique years from AQI-Cancer dataset
        years = aqi_cancer_df['Year'].unique()

        # Ensure Radon dataset has unique county entries
        radon_df = radon_df.drop_duplicates(subset=['County'])

        # Expand Radon data to match years in AQI-Cancer dataset
        expanded_radon_df = radon_df.loc[radon_df.index.repeat(len(years))].reset_index(drop=True)
        expanded_radon_df['Year'] = sorted(years.tolist() * len(radon_df))

        print("Radon dataset expanded to match AQI-Cancer dataset years.")

        # Merge the expanded Radon dataset with the AQI-Cancer dataset on 'County' and 'Year'
        merged_df = aqi_cancer_df.merge(expanded_radon_df, on=['County', 'Year'], how='left')

        # Ensure no duplicate counties for the same year
        merged_df = merged_df.drop_duplicates(subset=['County', 'Year'])

        # Save the merged dataset
        merged_df.to_csv(output_file_path, index=False)

        # Print dataset shape
        num_rows, num_columns = merged_df.shape
        print(f"\nMerged dataset saved as: {output_file_path}")
        print(f"Total Rows: {num_rows}, Total Columns: {num_columns}")

        # Print column names
        print("\nAll Columns in Merged Dataset:")
        print(list(merged_df.columns))

        # Print first 10 rows
        print("\nFirst 10 Rows of Merged Dataset:")
        print(merged_df.head(10))

        return output_file_path

    except Exception as e:
        print(f"Error during merging: {e}")
        return None

if __name__ == "__main__":
    merge_radon_aqi_cancer()
