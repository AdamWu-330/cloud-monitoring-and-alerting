/*
Here are links to help you get started with Stream Analytics Query Language:
Common query patterns - https://go.microsoft.com/fwLink/?LinkID=619153
Query language - https://docs.microsoft.com/stream-analytics-query/query-language-elements-azure-stream-analytics
*/
SELECT
    timestamp,
    metric_name,
    AnomalyDetection_SpikeAndDip(CAST(value as float), 99, 100, 'spikes') OVER (LIMIT DURATION(minute, 5)) AS SpikeDipDetection,
    AnomalyDetection_ChangePoint(CAST(value as float), 90, 100) OVER (LIMIT DURATION(minute, 5)) AS ChangePointDetection
INTO
    networkoutput
FROM
    networkinput TIMESTAMP BY timestamp
WHERE
    metric_name = 'node_network_receive_bytes_total'