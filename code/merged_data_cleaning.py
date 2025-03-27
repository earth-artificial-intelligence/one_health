import os
import pandas as pd

# Define the directory where the dataset is stored
TARGET_DIRECTORY = "/media/volume1"

# Define file paths
FINAL_MERGED_FILE_PATH = os.path.join(TARGET_DIRECTORY, "final_merged_dataset.csv")
CLEANED_FILE_PATH = os.path.join(TARGET_DIRECTORY, "cleaned_final_merged_dataset.csv")

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
        print("Dataset loaded successfully.")
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

def clean_dataset(df):
    """
    Cleans the dataset by:
    1. Dropping 'State_y'.
    2. Renaming 'State_x' to 'State'.

    Args:
        df (pd.DataFrame): The dataset to clean.

    Returns:
        pd.DataFrame: Cleaned dataset.
    """
    try:
        # Drop 'State_y' if it exists
        if "State_y" in df.columns:
            df.drop(columns=["State_y"], inplace=True)

        # Rename 'State_x' to 'State' if it exists
        if "State_x" in df.columns:
            df.rename(columns={"State_x": "State"}, inplace=True)

        print("Dataset cleaned successfully.")
        return df
    except Exception as e:
        print(f"Error during cleaning: {e}")
        return None

def save_cleaned_dataset(df, file_path):
    """
    Saves the cleaned dataset to the specified file path.

    Args:
        df (pd.DataFrame): The cleaned dataset.
        file_path (str): Path to save the cleaned dataset.
    """
    try:
        df.to_csv(file_path, index=False)
        print(f"Cleaned dataset saved successfully as '{file_path}'.")
    except Exception as e:
        print(f"Error saving dataset: {e}")

def print_dataset_info(df):
    """
    Prints the dataset's column names and first 10 rows.

    Args:
        df (pd.DataFrame): The dataset to print.
    """
    print("\nAll Columns in Cleaned Dataset:")
    print(list(df.columns))

    print("\nFirst 10 Rows of Cleaned Dataset:")
    print(df.head(10))

def main():
    """
    Main function to load, clean, and save the dataset.
    """
    df = load_dataset(FINAL_MERGED_FILE_PATH)
    if df is not None:
        cleaned_df = clean_dataset(df)
        if cleaned_df is not None:
            save_cleaned_dataset(cleaned_df, CLEANED_FILE_PATH)
            print_dataset_info(cleaned_df)  # Print columns and first 10 rows

if __name__ == "__main__":
    main()
