import os
import pandas as pd

# Define the directory where datasets are stored
TARGET_DIRECTORY = "/media/volume1"

# Define file paths
CLEANED_FINAL_DATA_PATH = os.path.join(TARGET_DIRECTORY, "cleaned_final_merged_dataset.csv")
BIRDS_DATA_PATH = os.path.join(TARGET_DIRECTORY, "hpai-wild-birds-2022.csv")
OUTPUT_FILE_PATH = os.path.join(TARGET_DIRECTORY, "final_merged_with_birds.csv")

def load_dataset(file_path):
    """
    Loads the dataset from the given file path.

    Args:
        file_path (str): Path to the dataset.

    Returns:
        pd.DataFrame: Loaded pandas DataFrame.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None

    try:
        df = pd.read_csv(file_path)
        print(f"Dataset loaded successfully from {file_path}")
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

def merge_datasets(aqi_cancer_df, birds_df):
    """
    Merges the AQI-Cancer dataset with the Birds dataset based on 'County'.
    Retains the 'State' column from AQI-Cancer data.
    Removes duplicate 'County' and 'State' columns from the Birds dataset.

    Args:
        aqi_cancer_df (pd.DataFrame): The cleaned AQI-Cancer dataset.
        birds_df (pd.DataFrame): The birds dataset.

    Returns:
        pd.DataFrame: Merged dataset.
    """
    try:
        # Keep a copy of the State column from AQI-Cancer dataset
        if "State" in aqi_cancer_df.columns:
            state_map = aqi_cancer_df.set_index("County")["State"].to_dict()
        
        # Merge datasets on 'County', keeping all columns (fill missing values with NaN)
        merged_df = aqi_cancer_df.merge(birds_df, on="County", how="left")

        # Restore the 'State' column from AQI-Cancer dataset
        if "State" in aqi_cancer_df.columns:
            merged_df["State"] = merged_df["County"].map(state_map)

        # Drop the duplicate 'County' and 'State' columns from the Birds dataset
        columns_to_drop = [col for col in ["State_x", "State_y"] if col in merged_df.columns]
        merged_df.drop(columns=columns_to_drop, errors="ignore", inplace=True)

        print("Datasets merged successfully.")
        return merged_df
    except Exception as e:
        print(f"Error during merging: {e}")
        return None

def reorder_columns(df):
    """
    Moves the 'State' column to the first position.

    Args:
        df (pd.DataFrame): The dataset to reorder.

    Returns:
        pd.DataFrame: Dataset with 'State' as the first column.
    """
    if "State" in df.columns:
        column_order = ["State"] + [col for col in df.columns if col != "State"]
        df = df[column_order]
        print("Moved 'State' column to the first position.")
    else:
        print("Warning: 'State' column not found in dataset.")
    
    return df

def save_dataset(df, file_path):
    """
    Saves the merged dataset to the specified file path.

    Args:
        df (pd.DataFrame): The merged dataset.
        file_path (str): Path to save the dataset.
    """
    try:
        df.to_csv(file_path, index=False)
        print(f"Merged dataset saved successfully as '{file_path}'.")
    except Exception as e:
        print(f"Error saving dataset: {e}")

def print_dataset_info(df):
    """
    Prints the dataset's column names, first 10 rows, and total number of rows and columns.

    Args:
        df (pd.DataFrame): The dataset to print.
    """
    num_rows, num_columns = df.shape
    print(f"\nTotal Rows: {num_rows}, Total Columns: {num_columns}")

    print("\nAll Columns in Merged Dataset:")
    print(list(df.columns))

    print("\nFirst 10 Rows of Merged Dataset:")
    print(df.head(10))

def main():
    """
    Main function to load, merge, reorder, save, and print dataset information.
    """
    aqi_cancer_df = load_dataset(CLEANED_FINAL_DATA_PATH)
    birds_df = load_dataset(BIRDS_DATA_PATH)

    if aqi_cancer_df is not None and birds_df is not None:
        merged_df = merge_datasets(aqi_cancer_df, birds_df)
        if merged_df is not None:
            merged_df = reorder_columns(merged_df)  # Move 'State' column to first position
            save_dataset(merged_df, OUTPUT_FILE_PATH)
            print_dataset_info(merged_df)  # Print dataset info after merging

if __name__ == "__main__":
    main()
