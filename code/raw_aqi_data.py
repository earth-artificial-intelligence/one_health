import os
import pandas as pd
import zipfile
from download_data_utils import download_file  

# Define the base directory to save files
TARGET_DIRECTORY = "/media/volume1"

# Ensure the directory exists
os.makedirs(TARGET_DIRECTORY, exist_ok=True)

# Dictionary of URLs for all years
AQI_DATA_URLS = {
    2017: "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2017.zip",
    2018: "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2018.zip",
    2019: "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2019.zip",
    2020: "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2020.zip",
    2021: "https://aqs.epa.gov/aqsweb/airdata/annual_aqi_by_county_2021.zip",
}

def retrieve_aqi(year):
    """
    Downloads the AQI ZIP file for a given year, extracts the CSV, and saves it to /media/volume1.
    """
    zip_file_path = os.path.join(TARGET_DIRECTORY, f"annual_aqi_by_county_{year}.zip")
    extracted_csv_path = os.path.join(TARGET_DIRECTORY, f"annual_aqi_by_county_{year}.csv")

    # Get the download URL
    original_url = AQI_DATA_URLS.get(year)
    if not original_url:
        print(f"No URL found for year {year}. Skipping...")
        return

    # Download the ZIP file
    saved_file = download_file(original_url, TARGET_DIRECTORY, f"annual_aqi_by_county_{year}.zip")

    if saved_file and os.path.exists(saved_file):
        try:
            # Extract the ZIP file
            with zipfile.ZipFile(saved_file, "r") as zip_ref:
                zip_ref.extractall(TARGET_DIRECTORY)
                extracted_files = zip_ref.namelist()  # Get extracted file names

            # Identify the correct CSV file
            csv_file_name = next((f for f in extracted_files if f.endswith(".csv")), None)
            if csv_file_name:
                extracted_csv_path = os.path.join(TARGET_DIRECTORY, csv_file_name)

                # Load CSV into pandas
                df = pd.read_csv(extracted_csv_path)

                # Print a few rows to verify
                print(f"AQI Data for {year} extracted and saved as: {extracted_csv_path}")
                print("\nAQI Data Preview:")
                print(df.head())  # Prints the first 5 rows
            else:
                print(f"No CSV file found in the ZIP archive for {year}.")

        except Exception as e:
            print(f"Error extracting or loading AQI Data for {year}: {e}")
    else:
        print(f"AQI data download failed for {year}. Please check the URL and permissions.")

def retrieve_all_years():
    """
    Downloads and processes AQI data for all specified years.
    """
    for year in AQI_DATA_URLS.keys():
        retrieve_aqi(year)

if __name__ == "__main__":
    retrieve_all_years()
