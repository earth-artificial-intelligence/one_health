import os
import pandas as pd
from download_data_utils import download_file  

def retrieve_cancer_data():
    """
    Downloads the cancer incidence data and loads it into a pandas DataFrame.
    """
    # Define the target directory
    target_directory = "/media/volume1"

    # Ensure the directory exists
    os.makedirs(target_directory, exist_ok=True)

    # Define the URL for cancer data
    cancer_data_url = "https://www.statecancerprofiles.cancer.gov/incidencerates/index.php?stateFIPS=00&areatype=county&cancer=047&race=00&sex=0&age=001&stage=999&type=incd&sortVariableName=rate&sortOrder=desc&output=1"

    # Define the expected filename
    cancer_file_name = "incd.csv"
    cancer_file_path = os.path.join(target_directory, cancer_file_name)

    # Download the file
    saved_file = download_file(cancer_data_url, target_directory, cancer_file_name)

    if saved_file and os.path.exists(saved_file):
        # Load the CSV file while skipping the first 8 empty rows
        cancer_data = pd.read_csv(saved_file, skiprows=8)

        # Print the first few rows
        print("Cancer Data Preview:")
        print(cancer_data.head())  # Prints the first 5 rows
    else:
        print("Cancer data download failed. Please check the URL and permissions.")

if __name__ == "__main__":
    retrieve_cancer_data()
