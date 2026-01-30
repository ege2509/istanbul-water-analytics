
CREATE VIEW dam_rolling_averages AS
SELECT
	date,
	dam_id,
	precipitation_m3,
	occupancy_m3,
	AVG(precipitation_m3) OVER (
        PARTITION BY dam_id 
        ORDER BY date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS precipitation_7day_avg,
	AVG(precipitation_m3) OVER (
        PARTITION BY dam_id 
        ORDER BY date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS precipitation_30day_avg,

	AVG(precipitation_m3) OVER (
        PARTITION BY dam_id 
        ORDER BY date 
        ROWS BETWEEN 89 PRECEDING AND CURRENT ROW
    ) AS precipitation_90day_avg,

	AVG(occupancy_m3) OVER (
        PARTITION BY dam_id 
        ORDER BY date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS occupancy_7day_avg,
	AVG(occupancy_m3) OVER (
        PARTITION BY dam_id 
        ORDER BY date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS occupancy_30day_avg,

	AVG(occupancy_m3) OVER (
        PARTITION BY dam_id 
        ORDER BY date 
        ROWS BETWEEN 89 PRECEDING AND CURRENT ROW
    ) AS occupancy_90day_avg
FROM daily_dam

