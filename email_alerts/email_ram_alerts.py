from azure.storage.blob import BlobServiceClient
import json
import smtplib
from email.mime.text import MIMEText

# Azure Blob Storage details
storage_account_name = 'blobstorage1779'
storage_account_key = '4LnGvstALk+i0TxyrHliGD1cMWX9tXdWi1cZEqYYlA/DVXQXQPNWkXMSE3BLdnwhx632Py4kxA0v+AStGx4ICQ=='
container_name = 'ramoutput'

# Email details (for example using SMTP)
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # or another port
smtp_user = 'ece1779.team23'
smtp_password = 'wbohkmpfeggipjgu'
sender_email = 'ece1779.team23@gmail.com'
# receiver_email = 'adamshuangwu@gmail.com'
receivers_email = ['adamshuangwu@gmail.com', 'boshen.zhang@mail.utoronto.ca', 'yuqi.yang@mail.utoronto.ca']
#receiver_email = 'boshen.zhang@mail.utoronto.ca'

# Connect to Azure Blob Storage
blob_service_client = BlobServiceClient(account_url=f"https://{storage_account_name}.blob.core.windows.net", credential=storage_account_key)
container_client = blob_service_client.get_container_client(container_name)

# Get the latest blob
blobs = container_client.list_blobs()
latest_blob = max(blobs, key=lambda x: x['last_modified'])

# # Download the latest blob
blob_client = container_client.get_blob_client(latest_blob.name)
blob_data = blob_client.download_blob().readall()
#print(blob_data)
blob_str = blob_data.decode('utf-8')
# print(blob_str)

anomaly_detected = False

email_content = []
for json_obj in blob_str.strip().split('\n'):  # Assuming each JSON object is on a new line
    try:
        data = json.loads(json_obj)
        if data['SpikeDipDetection']['IsAnomaly'] == 1:
            email_content.append(json.dumps(data))
            anomaly_detected = True
        # Process individual JSON object
    except json.JSONDecodeError:
        # Handle JSON decode error
        pass
    
# data = json.loads(blob_str)
email_content = '\n'.join(email_content)
# print(email_content)

if anomaly_detected:
    # print('detected')
    for receiver_email in receivers_email:
        # Create email message
        msg = MIMEText(email_content)
        msg['Subject'] = 'RAM Anomaly Alert'
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print('Email sent!')
