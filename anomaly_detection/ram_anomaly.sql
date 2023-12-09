/*
Here are links to help you get started with Stream Analytics Query Language:
Common query patterns - https://go.microsoft.com/fwLink/?LinkID=619153
Query language - https://docs.microsoft.com/stream-analytics-query/query-language-elements-azure-stream-analytics
*/
SELECT
    timestamp,
    metric_name,
    CAST(value as float) as value,
    AnomalyDetection_SpikeAndDip(CAST(value as float), 70, 10, 'spikes') OVER (LIMIT DURATION(minute, 5)) AS SpikeDipDetection
INTO
    ramoutput
FROM
    raminput TIMESTAMP BY timestamp
WHERE
    metric_name = 'occupied_ram_percentage'