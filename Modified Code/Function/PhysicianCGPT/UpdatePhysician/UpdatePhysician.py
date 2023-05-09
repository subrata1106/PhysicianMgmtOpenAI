

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
        conn_str="DefaultEndpointsProtocol=https;AccountName=physicianlist;AccountKey=4IQm0c5oQaXSYqOVd8x4O9bc46PJHk0xtk8O9z6GugyIb0fbuTEf11Ez8Y9CYsMGbjlRA/ohCdDF+AStbSl/gw==;EndpointSuffix=core.windows.net") #updated
    # Get the container client
    container_client = blob_service_client.get_container_client("physicians")
    # Get the blob client
    blob_client = container_client.get_blob_client("Physicians.json") #updated
    # Download the content
    blob_content = blob_client.download_blob().readall()
    # Load the content as JSON
    physicians = json.loads(blob_content)
    # Find the physician
    physician = next((p for p in physicians["physicians"] if p['id'] == physician_id), None)  ##updated physicians to physicians["physicians"] 
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
    blob_client.upload_blob(json.dumps(physicians),overwrite=True) #updated
    # Return the Physicians.json data in the response
    return func.HttpResponse(
        body=json.dumps(physicians),
        status_code=200, mimetype="application/json"
    )