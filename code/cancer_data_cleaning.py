import pandas as pd
import os

# Define the directory where the cancer data file is stored
TARGET_DIRECTORY = "/media/volume1"  

# File paths
RAW_FILE_PATH = os.path.join(TARGET_DIRECTORY, "incd.csv")
CLEANED_FILE_PATH = os.path.join(TARGET_DIRECTORY, "cleaned_cancer_data.csv")
FINAL_CLEANED_FILE_PATH = os.path.join(TARGET_DIRECTORY, "updated_cleaned_cancer.csv")

def clean_cancer_data():
    """
    Cleans the cancer incidence dataset by:
    1. Removing the first 8 blank rows.
    2. Removing unnecessary columns.
    3. Splitting 'County' column into 'County Name' and 'State Name'.
    4. Reordering columns for clarity.
    5. Printing the first few rows for verification.
    """
    if not os.path.exists(RAW_FILE_PATH):
        print(f" Error: {RAW_FILE_PATH} does not exist.")
        return None

    try:
        # Step 1: Read the data while skipping the first 8 rows
        df = pd.read_csv(RAW_FILE_PATH, skiprows=8, skip_blank_lines=True)
        print(" Initial dataset loaded with first 8 rows removed.")

        # Step 2: Drop unnecessary columns
        columns_to_drop = [
            "FIPS", 
            "CI*Rank([rank note])", 
            "Lower CI (CI*Rank)", 
            "Upper CI (CI*Rank)"
        ]
        df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)
        print(" Unnecessary columns removed.")

        # Save intermediate cleaned dataset
        df.to_csv(CLEANED_FILE_PATH, index=False)
        print(f" Cleaned dataset saved to: {CLEANED_FILE_PATH}")

        # Step 3: Further cleaning - Split 'County' into 'County Name' and 'State Name'
        if "County" in df.columns:
            df[['County Name', 'State Name']] = df['County'].str.extract(r'^(.*) County, (.*)\(\d+\)$')
            df.drop(columns=['County'], inplace=True)
            print(" 'County' column split into 'County Name' and 'State Name'.")

        # Step 4: Reorder columns for better readability
        if "State Name" in df.columns and "County Name" in df.columns:
            columns_order = ["State Name", "County Name"] + [col for col in df.columns if col not in ["State Name", "County Name"]]
            df = df[columns_order]
            print(" Columns reordered.")

        # Save final cleaned dataset
        df.to_csv(FINAL_CLEANED_FILE_PATH, index=False)
        print(f"\n Final cleaned dataset saved as: {FINAL_CLEANED_FILE_PATH}")

        # Print first few rows of the cleaned dataset
        print("\n Cleaned Data Preview:")
        print(df.head())  # Prints the first 5 rows

        return FINAL_CLEANED_FILE_PATH

    except Exception as e:
        print(f" Error during data cleaning: {e}")
        return None

if __name__ == "__main__":
    clean_cancer_data()
