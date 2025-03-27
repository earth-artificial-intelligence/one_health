import pandas as pd
import os

# Define the directory where the cleaned datasets are stored
TARGET_DIRECTORY = "/media/volume1"

# Define file paths
aqi_file_path = os.path.join(TARGET_DIRECTORY, "merged_annual_aqi_by_county.csv")
cancer_file_path = os.path.join(TARGET_DIRECTORY, "updated_cleaned_cancer.csv")
output_file_path = os.path.join(TARGET_DIRECTORY, "merged_aqi_cancer.csv")

def merge_aqi_cancer_data():
    """
    Merges the updated cleaned cancer dataset with the merged AQI dataset.
    Expands the cancer data to match all years in the AQI dataset.
    """
    if not os.path.exists(aqi_file_path):
        print(f" Error: AQI file '{aqi_file_path}' not found.")
        return None

    if not os.path.exists(cancer_file_path):
        print(f" Error: Cancer file '{cancer_file_path}' not found.")
        return None

    try:
        # Load the datasets
        aqi_df = pd.read_csv(aqi_file_path)
        cancer_df = pd.read_csv(cancer_file_path)

        print(" Datasets loaded successfully.")

        # Standardizing column names for merging
        cancer_df.rename(columns={'State Name': 'State', 'County Name': 'County'}, inplace=True)

        # Keeping relevant columns from the cancer dataset
        cancer_df = cancer_df[['State', 'County'] + [col for col in cancer_df.columns if col not in ['State', 'County']]]

        # Extracting the unique years from the AQI dataset
        years = aqi_df['Year'].unique()

        # Expanding the cancer dataset by duplicating each row for every year in AQI dataset
        cancer_expanded_df = cancer_df.loc[cancer_df.index.repeat(len(years))].reset_index(drop=True)

        # Assigning years by repeating the entire list for the correct number of rows
        cancer_expanded_df['Year'] = years.tolist() * (len(cancer_expanded_df) // len(years))

        print(" Cancer dataset expanded to match AQI dataset years.")

        # Merging the expanded cancer dataset with the AQI dataset
        merged_df = pd.merge(aqi_df, cancer_expanded_df, on=['State', 'County', 'Year'], how='left')

        # Save the merged dataset
        merged_df.to_csv(output_file_path, index=False)

        print(f"\n Merged dataset saved as: {output_file_path}")
        print("\n Merged Data Preview:")
        print(merged_df.head())  # Print the first few rows

        return output_file_path

    except Exception as e:
        print(f" Error during merging: {e}")
        return None

if __name__ == "__main__":
    merge_aqi_cancer_data()
