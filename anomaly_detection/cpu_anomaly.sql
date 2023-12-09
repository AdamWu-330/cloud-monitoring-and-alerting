/*
Here are links to help you get started with Stream Analytics Query Language:
Common query patterns - https://go.microsoft.com/fwLink/?LinkID=619153
Query language - https://docs.microsoft.com/stream-analytics-query/query-language-elements-azure-stream-analytics
*/
SELECT
    timestamp,
    metric_name,
    CAST(value as float) as cpu_usage_value,
    AnomalyDetection_SpikeAndDip(CAST(value as float), 99, 100, 'spikes') OVER (LIMIT DURATION(minute, 5)) AS SpikeDipDetection,
    AnomalyDetection_ChangePoint(CAST(value as float), 90, 100) OVER (LIMIT DURATION(minute, 5)) AS ChangePointDetection
INTO
    cpuoutput
FROM
    cpuinput TIMESTAMP BY timestamp
WHERE
    metric_name = 'total_non_idle_cpu_usage'
