import os
import csv
import pytz
import json
from datetime import datetime
from script import scrape_jobs 
from apscheduler.schedulers.background import BackgroundScheduler
from azure.storage.blob import BlobServiceClient, BlobClient
import logging

# Azure credentials
account_name = "practiceaccount9090"
account_key = "1GWxliSYnnPq5+RHpmktxukFo/Kuv9uab5tfnz/59lyfPYGZ9PIY9adx/BkV+MCpJh2sjSe2ENsR+AStuUrPYw=="

# Blob container
container_name = "scraping-container"

# Initialize blob service
blob_service_client = BlobServiceClient(
    account_url=f"https://{account_name}.blob.core.windows.net",
    credential=account_key
)

file='job_data.csv'
index = 5

def generate_and_upload_csv():
    # logging.info("Enter to generate_and_upload_csv")
    print("Enter to generate_and_upload_csv")
    scrape_jobs()
    global index, rows

    # Update data
    index += 1

    # Generate CSV
    # Set the Pakistan time zone
    pakistan_tz = pytz.timezone('Asia/Karachi')

    current_time = datetime.now(pakistan_tz)
    filename = f"data_{index}.csv"

    # Upload CSV to blob
    blob_client_csv = blob_service_client.get_blob_client(container=container_name, blob=filename)

    with open(file, "rb") as data:
        blob_client_csv.upload_blob(data)

    # Delete the local CSV file
    os.remove(file)
    
    # Create or update JSON file
    json_data = {
        'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'filename': filename,
        'website':'http://dailyremote.com'
    }

    json_file = 'files.json'

    # Check if JSON file exists in blob storage
    blob_client_json = blob_service_client.get_blob_client(container=container_name, blob=json_file)
    json_file_exists = blob_client_json.exists()

    if json_file_exists:
        # Download existing JSON file
        existing_json_blob = blob_client_json.download_blob()
        existing_json_data = json.loads(existing_json_blob.content_as_text())

        # Append new data to existing JSON data
        existing_json_data.append(json_data)
        updated_json_data = existing_json_data
    else:
        # Create new JSON data with only the current record
        updated_json_data = [json_data]

    # Upload updated JSON data to blob storage
    updated_json_text = json.dumps(updated_json_data)
    blob_client_json.upload_blob(updated_json_text, overwrite=True)

    print(f"Generated and uploaded {filename} to blob")
    print(f"Appended data to {json_file} and uploaded to blob")
    print("Exit to generate_and_upload_csv")

generate_and_upload_csv()


# Schedule job
scheduler = BackgroundScheduler()
scheduler.add_job(generate_and_upload_csv, 'interval', days=3)
scheduler.start()

# Keep the script running to allow the scheduler to work
try:
    while True:
        pass
except KeyboardInterrupt:
    scheduler.shutdown()
