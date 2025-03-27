import os
import pandas as pd

# Define the directory where the dataset is stored
TARGET_DIRECTORY = "/media/volume1"

# Define file paths
BIRDS_DATA_FILE_PATH = os.path.join(TARGET_DIRECTORY, "hpai-wild-birds.csv")
CLEANED_BIRDS_FILE_PATH = os.path.join(TARGET_DIRECTORY, "hpai-wild-birds-2022.csv")

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

def filter_by_year(df, year=2022):
    """
    Filters the dataset to keep only rows where 'Date Detected' is in the specified year.

    Args:
        df (pd.DataFrame): The dataset to filter.
        year (int): The year to keep.

    Returns:
        pd.DataFrame: Filtered dataset.
    """
    try:
        # Ensure 'Date Detected' column exists
        if "Date Detected" not in df.columns:
            print("Error: 'Date Detected' column not found in dataset.")
            return None

        # Convert 'Date Detected' column to datetime format
        df["Date Detected"] = pd.to_datetime(df["Date Detected"], errors="coerce")

        # Filter only rows where the year is 2022
        df_filtered = df[df["Date Detected"].dt.year == year]

        print(f"Dataset filtered to keep only rows from {year}.")
        return df_filtered
    except Exception as e:
        print(f"Error during filtering: {e}")
        return None

def save_filtered_dataset(df, file_path):
    """
    Saves the filtered dataset to the specified file path.

    Args:
        df (pd.DataFrame): The filtered dataset.
        file_path (str): Path to save the dataset.
    """
    try:
        df.to_csv(file_path, index=False)
        print(f"Filtered dataset saved successfully as '{file_path}'.")
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

    print("\nAll Columns in Filtered Dataset:")
    print(list(df.columns))

    print("\nFirst 10 Rows of Filtered Dataset:")
    print(df.head(10))

def main():
    """
    Main function to load, filter, save, and print dataset information.
    """
    df = load_dataset(BIRDS_DATA_FILE_PATH)
    if df is not None:
        filtered_df = filter_by_year(df, 2022)
        if filtered_df is not None:
            save_filtered_dataset(filtered_df, CLEANED_BIRDS_FILE_PATH)
            print_dataset_info(filtered_df)  # Print columns, first 10 rows, and dataset size

if __name__ == "__main__":
    main()
