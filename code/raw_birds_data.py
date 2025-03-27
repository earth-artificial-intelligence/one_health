import os
import pandas as pd
from download_data_utils import download_file  

def retrieve_birds_data():
    """
    Downloads the birds dataset and loads it into a pandas DataFrame.
    """
    # Define the target directory
    target_directory = "/media/volume1"

    # Ensure the directory exists
    os.makedirs(target_directory, exist_ok=True)

    # Define the URL for birds data
    birds_data_url = "https://huggingface.co/datasets/Geoweaver/animal_data/resolve/main/hpai-wild-birds.csv?download=true"

    # Define the expected filename
    birds_file_name = "hpai-wild-birds.csv"
    birds_file_path = os.path.join(target_directory, birds_file_name)

    # Download the file
    saved_file = download_file(birds_data_url, target_directory, birds_file_name)

    if saved_file and os.path.exists(saved_file):
        # Load the CSV file
        birds_data = pd.read_csv(saved_file)

        # Print the first few rows
        print("Birds Data Preview:")
        print(birds_data.head())  # Prints the first 5 rows
    else:
        print("Birds data download failed. Please check the URL and permissions.")

if __name__ == "__main__":
    retrieve_birds_data()
