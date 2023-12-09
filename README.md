# cloud-monitoring-and-alerting
The project for the course ECE1779 (Introduction to Cloud Computing) at University of Toronto

The project collects real-time metrics from an Azure Linux VM using node_exporter. A set of open source traffic generation tools are utilized (i.e., iperf3, stree) to simulate both normal and abnormal traffic. The metrics are sent to two platforms for analysis: Grafana and Azure Stream Analysis. For sending metrics to Grafana, Prometheus is used. For sending metrics to Azure Stream Analysis, a set of Python scripts takes the responsibility. 

On Grafana, a dynamic dashboard is created to visualize metrics, and alert rules based on threshold are created. For Azure Stream Analysis, anomaly detection is performed, using built-in functions of Azure queries. For the results of both platforms, emails will be sent to users to notify them of the alerts.

A breakdown of each folder:

anomaly_detection: queries used for each metric for Azure Stream Analytics to perform anomaly detection.

email_alerts: scripts to send emails for alert notification

node_exporter: node_exporter source tar file to be installed on the VM

prometheus: a prometheus config file for running prometheus that sends metrics to Grafana

send_metrics_to_azure: Pythons scripts running on the VM continuously to send real-time metrics to Azure 

simulate_traffic: tools or commands used to simulate traffic on the VM