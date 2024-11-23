import os
import requests
import gzip

# Variables
REDFIN_FILE_URL = "https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/city_market_tracker.tsv000.gz"
RAW_DIR = "../../data/raw"
UNZIPPED_FILE_PATH = os.path.join(RAW_DIR, "city_market_tracker.tsv")

def download_and_unzip_file(url, dest_path):
    """Download a compressed file from a URL, unzip it, and save the unzipped data."""
    print("Downloading and unzipping data from Redfin...")
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with gzip.GzipFile(fileobj=response.raw) as gz_file:
                with open(dest_path, "wb") as out_file:
                    out_file.write(gz_file.read())
            print(f"Download and unzip successful. File saved as {dest_path}.")
        else:
            print(f"Failed to download the file. HTTP Status Code: {response.status_code}")
            raise Exception("Download failed")
    except Exception as e:
        print(f"An error occurred during download or unzip: {e}")
        raise

def main():
    try:
        # Step 1: Download and unzip the file
        download_and_unzip_file(REDFIN_FILE_URL, UNZIPPED_FILE_PATH)

        print(f"The unzipped data is saved locally at: {UNZIPPED_FILE_PATH}")

    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
