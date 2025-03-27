import pandas as pd
import os

# Define the directory where the radon dataset is stored
TARGET_DIRECTORY = "/media/volume1"

# Define file paths
RAW_RADON_FILE_PATH = os.path.join(TARGET_DIRECTORY, "radon_zones.csv")
CLEANED_RADON_FILE_PATH = os.path.join(TARGET_DIRECTORY, "cleaned_radon_zones.csv")

# Dictionary to map state abbreviations to full names
STATE_ABBREVIATIONS = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
    "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"
}

def clean_radon_data():
    """
    Cleans the Radon dataset by:
    1. Extracting 'State' and 'County' from 'County,State' column.
    2. Keeping only the 'State', 'County', 'Region', and 'Zone' columns.
    3. Converting state abbreviations to full names.
    4. Removing the 2nd and 3rd rows.
    5. Printing the cleaned columns and first 5 rows.
    """
    if not os.path.exists(RAW_RADON_FILE_PATH):
        print(f"Error: Radon file '{RAW_RADON_FILE_PATH}' not found.")
        return None

    try:
        # Load the dataset
        df = pd.read_csv(RAW_RADON_FILE_PATH)

        print("Initial Radon dataset loaded.")

        # Step 1: Extract 'State' and 'County' from 'County,State'
        df[['County', 'State']] = df['County,State'].str.split(',', expand=True)

        # Trim whitespace in 'State' and 'County'
        df['State'] = df['State'].str.strip()
        df['County'] = df['County'].str.strip()

        # Step 2: Remove the 2nd and 3rd rows explicitly
        df.drop(index=[0, 1], inplace=True)
        df.reset_index(drop=True, inplace=True)  # Reset index after row removal
        print("Removed 2nd and 3rd rows from the dataset.")

        # Step 3: Convert State abbreviations to full names
        df['State'] = df['State'].map(STATE_ABBREVIATIONS).fillna(df['State'])
        print("State abbreviations converted to full state names.")

        # Step 4: Keep only relevant columns
        df = df[['State', 'County', 'Region', 'Zone']]
        print("Kept only required columns: State, County, Region, and Zone.")

        # Save the cleaned dataset
        df.to_csv(CLEANED_RADON_FILE_PATH, index=False)
        print(f"\nCleaned Radon dataset saved as: {CLEANED_RADON_FILE_PATH}")

        # Print all columns and first 5 rows
        print("\nCleaned Data Columns:")
        print(df.columns.tolist())
        print("\nCleaned Data Preview:")
        print(df.head())

        return CLEANED_RADON_FILE_PATH

    except Exception as e:
        print(f"Error during data cleaning: {e}")
        return None

if __name__ == "__main__":
    clean_radon_data()
