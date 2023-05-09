

import logging
import azure.functions as func
import json

from azure.storage.blob import BlobServiceClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Retrieve the connection string for use with the Blob Service Client
    connect_str = "<your_storage_account_connection_string>"

    # Create the Blob Service Client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Retrieve the container name
    container_name = "physicians"

    # Retrieve the blob name
    blob_name = "Physicians.json"

    # Retrieve the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Read the blob
    blob_data = blob_client.download_blob()
    blob_text = blob_data.readall()

    # Return the json in the response
    return func.HttpResponse(blob_text, mimetype="application/json")