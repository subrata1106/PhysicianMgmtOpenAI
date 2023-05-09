

import logging
import azure.functions as func
import json
from azure.storage.blob import BlobServiceClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get the request body
    req_body = req.get_json()

    # Get the Physician ID
    physician_id = req_body.get('physician_id')

    # Get the Clinic Name
    clinic_name = req_body.get('clinic_name')

    # Get the attending status
    attending_status = req_body.get('attending_status')

    # Create the Blob Service Client
    blob_service_client = BlobServiceClient.from_connection_string(
        conn_str="<your_storage_connection_string>")

    # Get the container client
    container_client = blob_service_client.get_container_client("physicians")

    # Get the blob client
    blob_client = container_client.get_blob_client("Physicians.json")

    # Download the content
    blob_content = blob_client.download_blob().readall()

    # Load the content as JSON
    physicians = json.loads(blob_content)

    # Find the physician
    physician = next((p for p in physicians if p['id'] == physician_id), None)

    # Check if the physician was found
    if physician is None:
        return func.HttpResponse(
            "Physician not found",
            status_code=404
        )

    # Find the clinic
    clinic = next((c for c in physician['clinics'] if c['name'] == clinic_name), None)

    # Check if the clinic was found
    if clinic is None:
        return func.HttpResponse(
            "Clinic not found",
            status_code=404
        )

    # Update the attending status
    clinic['attending'] = attending_status

    # Upload the content
    blob_client.upload_blob(json.dumps(physicians))

    return func.HttpResponse(
        "Attending status updated successfully",
        status_code=200
    )