import requests
import datetime
import re
from azure.storage.blob import BlobServiceClient

# Azure Blob Storage details
connect_str = "DefaultEndpointsProtocol=https;AccountName=blobstorage1779;AccountKey=4LnGvstALk+i0TxyrHliGD1cMWX9tXdWi1cZEqYYlA/DVXQXQPNWkXMSE3BLdnwhx632Py4kxA0v+AStGx4ICQ==;EndpointSuffix=core.windows.net"
container_name = "raminput"
blob_name = 'ram.csv'

# The URL where the node_exporter exposes its metrics
metrics_url = "http://localhost:9100/metrics"

# Perform the HTTP request to get the metrics
response = requests.get(metrics_url)

# Check if the request was successful
if response.status_code == 200:
    # Initialize the BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    append_blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Fetch existing data in the blob
    try:
        append_blob_client.get_blob_properties()
    except Exception:
        append_blob_client.create_append_blob()
        headers = "timestamp,metric_name,value\n"
        append_blob_client.append_block(headers)

    # Split the text response into lines
    lines = response.text.strip().split('\n')
    new_data = ""

    # Iterate over each line in the response
    total, free = 0, 0
    
    for line in lines:
        # Skip any comment lines
        if line.startswith('#'):
            continue
        
        metric_name, value = line.split()[:2]
                     
        if metric_name in ["node_memory_MemTotal_bytes", "node_memory_MemFree_bytes"]:
            # Normalize the metric name
            metric_name = metric_name.replace('{device="eth0"}', '')
            if metric_name == "node_memory_MemTotal_bytes":
                total = float(value)
            else:
                free = float(value)
        
    if total > 0 and free > 0:
        occupied_percentage = 1 - free / total
        # Create a CSV formatted string
        timestamp = datetime.datetime.now().isoformat()
        new_data += f'{timestamp},{"occupied_ram_percentage"},{occupied_percentage}\n'

    # Upload the combined data to the blob
    if new_data:
        append_blob_client.append_block(new_data.encode())

    print("RAM Metrics have been uploaded to Azure Blob Storage")
else:
    print("Failed to retrieve metrics. Status code:", response.status_code)
    
    
    
