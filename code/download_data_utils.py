import os
import urllib.request
import urllib.parse

def download_file(url, save_location, file_name=None):
    """
    Downloads a file from a given URL and saves it to the specified location.

    Args:
        url (str): The URL of the file to download.
        save_location (str): The directory where the file should be saved.
        file_name (str, optional): The name to save the file as. 
                                   If None, the filename is extracted from the URL.
    
    Returns:
        str: Full path of the saved file if successful, None if failed.
    """
    try:
        print("Starting file download...")

        # Ensure the save directory exists
        os.makedirs(save_location, exist_ok=True)

        # Extract filename from URL if not provided
        if file_name is None:
            file_name = os.path.basename(url.split("?")[0])  # Remove URL parameters

        # Define the full save path
        save_path = os.path.join(save_location, file_name)

        # Open the URL and read the content
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                print(f"Failed to download file. HTTP Status: {response.status}")
                return None
            file_content = response.read()

        # Write the file
        with open(save_path, 'wb') as file:
            file.write(file_content)

        print(f"File downloaded successfully and saved as: {save_path}")
        return save_path  # Return the saved file path

    except Exception as e:
        print(f"An error occurred while downloading the file: {str(e)}")
        return None

