import os
import pandas as pd
from download_data_utils import download_file  

def retrieve_radon_data():
    """
    Downloads the Radon Zone Data (.xls), converts it to .csv, and saves it to /media/volume1.
    Then, prints a few rows of the converted data.
    """
    # Define the target directory
    target_directory = "/media/volume1"

    # Ensure the directory exists
    os.makedirs(target_directory, exist_ok=True)

    # Define the URL for Radon Zone data
    radon_data_url = "https://www.epa.gov/system/files/documents/2024-05/radon_zones-spreadsheet.xls"

    # Define file paths
    radon_xls_path = os.path.join(target_directory, "radon_zones.xls")
    radon_csv_path = os.path.join(target_directory, "radon_zones.csv")

    # Download the .xls file
    saved_file = download_file(radon_data_url, target_directory, "radon_zones.xls")

    if saved_file and os.path.exists(saved_file):
        try:
            # Read the .xls file into pandas
            df = pd.read_excel(saved_file, engine="xlrd")  # For .xls files

            # Convert to CSV
            df.to_csv(radon_csv_path, index=False)

            print(f"Radon Zone Data converted and saved as: {radon_csv_path}")

            # Print a few rows to verify
            print("\nRadon Zone Data Preview:")
            print(df.head())  # Prints the first 5 rows

        except Exception as e:
            print(f"Error converting Radon Zone Data: {e}")
    else:
        print("Radon Zone Data download failed. Please check the URL and permissions.")

if __name__ == "__main__":
    retrieve_radon_data()
