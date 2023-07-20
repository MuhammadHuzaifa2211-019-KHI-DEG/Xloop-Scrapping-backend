from flask import Flask, jsonify
from azure.storage.blob import BlobServiceClient
import json
import logging
from flask_cors import CORS

# Azure Blob Storage connection string and container name
# Azure credentials
account_name = "practiceaccount9090"
account_key = "1GWxliSYnnPq5+RHpmktxukFo/Kuv9uab5tfnz/59lyfPYGZ9PIY9adx/BkV+MCpJh2sjSe2ENsR+AStuUrPYw=="



# connection_string = 'your_connection_string'
container_name = "scraping-container"
json_file_name = 'files.json'

app = Flask(__name__)
cors = CORS(app)

@app.route('/api/jsonfile', methods=['GET'])
def get_json_file():
    try:
        print("Enter to get_json file")
        # Create BlobServiceClient
        # blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_service_client = BlobServiceClient(
        account_url=f"https://{account_name}.blob.core.windows.net",
        credential=account_key
    )

        # Get BlobClient for the JSON file
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=json_file_name)

        # Download the JSON file content
        file_content = blob_client.download_blob().content_as_text()
        json_obj = json.loads(file_content)
        print("Exit to get_json file")
        # Return the JSON file content as a response
        return jsonify(json_obj)

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(port=5000,host='0.0.0.0')
