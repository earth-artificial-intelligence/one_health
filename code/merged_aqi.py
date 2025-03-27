import os
import pandas as pd

# Define the directory where the AQI files are stored
TARGET_DIRECTORY = "/media/volume1"

# List of AQI CSV filenames for each year
AQI_FILES = [
    "annual_aqi_by_county_2017.csv",
    "annual_aqi_by_county_2018.csv",
    "annual_aqi_by_county_2019.csv",
    "annual_aqi_by_county_2020.csv",
    "annual_aqi_by_county_2021.csv"
]

def get_existing_files():
    """
    Checks which AQI files exist in the target directory.
    
    Returns:
        existing_files (list): List of valid CSV file paths.
        missing_files (list): List of missing CSV file paths.
    """
    csv_files = [os.path.join(TARGET_DIRECTORY, file) for file in AQI_FILES]
    
    existing_files = [file for file in csv_files if os.path.exists(file)]
    missing_files = [file for file in csv_files if not os.path.exists(file)]
    
    return existing_files, missing_files

def merge_aqi_files(existing_files):
    """
    Merges the available AQI CSV files into a single dataset.
    
    Args:
        existing_files (list): List of valid CSV file paths.

    Returns:
        merged_df (DataFrame): Merged Pandas DataFrame containing all AQI data.
    """
    print("\n Merging available AQI CSV files...")

    # Read and concatenate all existing CSV files
    df_list = [pd.read_csv(file) for file in existing_files]
    merged_df = pd.concat(df_list, ignore_index=True)

    return merged_df

def save_merged_data(merged_df):
    """
    Saves the merged AQI dataset to a CSV file.
    
    Args:
        merged_df (DataFrame): Merged Pandas DataFrame.
    """
    merged_file_path = os.path.join(TARGET_DIRECTORY, "merged_annual_aqi_by_county.csv")
    merged_df.to_csv(merged_file_path, index=False)

    print(f"\n Merged dataset saved as: {merged_file_path}")
    print("\nMerged Data Preview:")
    print(merged_df.head())  # Print the first few rows

def main():
    """
    Main function to check for available AQI files, merge them, and save the final dataset.
    """
    existing_files, missing_files = get_existing_files()

    if missing_files:
        print(f" The following files are missing and will not be included in the merge:")
        for missing_file in missing_files:
            print(f"   - {missing_file}")

    if existing_files:
        merged_df = merge_aqi_files(existing_files)
        save_merged_data(merged_df)
    else:
        print("\n No valid AQI files found to merge. Please check the file locations.")

if __name__ == "__main__":
    main()
