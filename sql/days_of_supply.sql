CREATE VIEW days_of_supply AS
SELECT
    ds.date,
    ds.total_occupancy_m3,
    ca.consumption_30day_avg,
    ds.total_occupancy_m3 / NULLIF(ca.consumption_30day_avg, 0) AS days_of_supply
FROM daily_system_metrics ds
LEFT JOIN consumption_averages ca
    ON ds.date = ca.date;