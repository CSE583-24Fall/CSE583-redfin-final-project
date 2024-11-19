#!/bin/bash

# Variables (replace these with your actual values)
REDFIN_FILE_URL="https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/city_market_tracker.tsv000.gz"
LOCAL_FILE_PATH="./city_market_tracker.tsv000.gz"
UNZIPPED_FILE_PATH="./city_market_tracker.tsv"
AZURE_STORAGE_ACCOUNT_NAME="redfinforcse583"
AZURE_CONTAINER_NAME="rawdatabucket"
AZURE_BLOB_NAME="city_market_tracker.tsv" # Adjusted blob name for original file without unique ID

# Download data from Redfin
echo "Downloading data from Redfin..."
curl -o "$LOCAL_FILE_PATH" "$REDFIN_FILE_URL"

# Check if the download was successful
if [ $? -eq 0 ]; then
    echo "Download successful. File saved as $LOCAL_FILE_PATH."
else
    echo "Failed to download the file. Exiting script."
    exit 1
fi

# Unzip the downloaded file
echo "Unzipping the file..."
gunzip -c "$LOCAL_FILE_PATH" > "$UNZIPPED_FILE_PATH"

# Check if unzipping was successful
if [ $? -eq 0 ]; then
    echo "Unzipping successful. File saved as $UNZIPPED_FILE_PATH."
else
    echo "Failed to unzip the file. Exiting script."
    exit 1
fi

# Upload the unmodified TSV file to Azure Blob Storage
echo "Uploading TSV file to Azure Blob Storage..."
az storage blob upload \
    --account-name "$AZURE_STORAGE_ACCOUNT_NAME" \
    --container-name "$AZURE_CONTAINER_NAME" \
    --name "$AZURE_BLOB_NAME" \
    --file "$UNZIPPED_FILE_PATH"

# Check if the upload was successful
if [ $? -eq 0 ]; then
    echo "File successfully uploaded to Azure Blob Storage."
else
    echo "Failed to upload the file to Azure Blob Storage."
    exit 1
fi

# Optional: Clean up local files
# rm "$LOCAL_FILE_PATH" "$UNZIPPED_FILE_PATH"
