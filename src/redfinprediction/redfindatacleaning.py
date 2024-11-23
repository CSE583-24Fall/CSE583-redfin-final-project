# Import necessary libraries
from azure.storage.blob import BlobServiceClient
import pandas as pd
import io


# Utility functions
def create_blob_service_client(storage_account_name, storage_account_access_key):
    return BlobServiceClient(
        account_url=f"https://{storage_account_name}.blob.core.windows.net/",
        credential=storage_account_access_key
    )


def get_container_client(blob_service_client, container_name):
    return blob_service_client.get_container_client(container_name)


def download_blob_to_dataframe(container_client, blob_name, separator='\t'):
    blob_client = container_client.get_blob_client(blob_name)
    stream = blob_client.download_blob()
    return pd.read_csv(io.BytesIO(stream.readall()), sep=separator, error_bad_lines=False)


def filter_dataframe_by_date(df, date_column, start_date):
    df[date_column] = pd.to_datetime(df[date_column])
    filtered_df = df[df[date_column] > start_date]
    filtered_df.dropna(inplace=True)
    return filtered_df


def save_dataframe_to_blob(container_client, dataframe, filename):
    output_stream = io.StringIO()
    dataframe.to_csv(output_stream, index=False)
    blob_client = container_client.get_blob_client(filename)
    blob_client.upload_blob(output_stream.getvalue(), overwrite=True)
    return filename


def save_metadata_to_blob(container_client, metadata_filename, data_filename, max_period_end_str):
    metadata_content = f"{data_filename}\n{max_period_end_str}"
    blob_client = container_client.get_blob_client(metadata_filename)
    blob_client.upload_blob(metadata_content, overwrite=True)


# Main function for the initial run
def process_initial_run(storage_account_name, storage_account_access_key, container_name, blob_name, start_date, output_folder):
    blob_service_client = create_blob_service_client(storage_account_name, storage_account_access_key)
    container_client = get_container_client(blob_service_client, container_name)

    df = download_blob_to_dataframe(container_client, blob_name)
    filtered_df = filter_dataframe_by_date(df, 'period_end', start_date)

    max_period_end = filtered_df['period_end'].max()
    max_period_end_str = max_period_end.strftime('%Y-%m-%d')
    output_filename = f"{output_folder}/city_market_tracker_after_{start_date}_{max_period_end_str}.csv"
    metadata_filename = f"{output_folder}/initial_run_filename.txt"

    save_dataframe_to_blob(container_client, filtered_df, output_filename)
    save_metadata_to_blob(container_client, metadata_filename, output_filename, max_period_end_str)

    print(f"Initial run completed. Data saved to: {output_filename}")
    print(f"Metadata saved to: {metadata_filename}")


# Example usage
if __name__ == "__main__":
    # Azure Blob Storage credentials
    storage_account_name = "redfinforcse583"
    storage_account_access_key = "Qid0jauQrk38wT+G7WDaJ1LQizsFQd+J8LV2hgsMA2/QmovEJX8c0RPtnfQjqAy2Izz2eTmwNXl2+ASt238BiQ=="
    container_name = "rawdatabucket"
    blob_name = "city_market_tracker.tsv"
    start_date = "2019-01-01"
    output_folder = "cleaned_data"

    process_initial_run(
        storage_account_name,
        storage_account_access_key,
        container_name,
        blob_name,
        start_date,
        output_folder
    )
