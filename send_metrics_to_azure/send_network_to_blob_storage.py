import requests
import datetime
from azure.storage.blob import BlobServiceClient

# Azure Blob Storage details
connect_str = "DefaultEndpointsProtocol=https;AccountName=blobstorage1779;AccountKey=4LnGvstALk+i0TxyrHliGD1cMWX9tXdWi1cZEqYYlA/DVXQXQPNWkXMSE3BLdnwhx632Py4kxA0v+AStGx4ICQ==;EndpointSuffix=core.windows.net"
container_name = "networkinput"
blob_name = 'network.csv'

# The URL where the node_exporter exposes its metrics
metrics_url = "http://localhost:9100/metrics"

# Perform the HTTP request to get the metrics
response = requests.get(metrics_url)

if response.status_code == 200:
    # Initialize the BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    append_blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Check if the blob exists and create if not, with headers
    try:
        append_blob_client.get_blob_properties()
    except Exception:
        append_blob_client.create_append_blob()
        headers = "timestamp,metric_name,value\n"
        append_blob_client.append_block(headers)

    lines = response.text.strip().split('\n')
    new_data = ""
    total_non_idle_cpu_usage = 0

    for line in lines:
        if line.startswith('#'):
            continue
        
        metric_name, value = line.split()[:2]
        
        #     # Only process metrics of interest
        if metric_name == 'node_network_receive_bytes_total{device="eth0"}':
            # Normalize the metric name
            metric_name = metric_name.replace('{device="eth0"}', '')
            # Create a CSV formatted string
            timestamp = datetime.datetime.now().isoformat()
            new_data += f'{timestamp},{metric_name},{value}\n'
    
    # Append the new data to the blob
    if new_data:
        append_blob_client.append_block(new_data.encode())

    print("network metrics have been uploaded to Azure Blob Storage")
else:
    print("Failed to retrieve metrics. Status code:", response.status_code)