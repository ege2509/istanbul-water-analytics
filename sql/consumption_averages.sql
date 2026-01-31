CREATE VIEW consumption_averages AS
SELECT
	date,
	consumption_m3,
	city_name,
	AVG(consumption_m3) OVER (
	    PARTITION BY city_name 
        ORDER BY date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
		) AS consumption_7day_avg,

	AVG(consumption_m3) OVER (
	    PARTITION BY city_name 
        ORDER BY date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
		) AS consumption_30day_avg,
	AVG(consumption_m3) OVER (
	    PARTITION BY city_name 
        ORDER BY date 
        ROWS BETWEEN 89 PRECEDING AND CURRENT ROW
		) AS consumption_90day_avg
FROM city_consumption
