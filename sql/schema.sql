CREATE TABLE dams (
id SERIAL PRIMARY KEY,
    dam_name VARCHAR(50) NOT NULL UNIQUE,
    max_capacity_m3 DECIMAL(12, 2) NOT NULL
)

CREATE TABLE daily_dam (
id SERIAL PRIMARY KEY,
    dam_id INTEGER NOT NULL REFERENCES dams(id),
	precipitation_pct DECIMAL(5, 2),
	precipitation_m3 DECIMAL(12,2),
	occupancy_pct DECIMAL(5,2),
	occupancy_m3 DECIMAL(12,2),
	date DATE
)

CREATE TABLE city_consumption (
id SERIAL PRIMARY KEY,
	city_name TEXT,
	consumption_m3 INTEGER
	date DATE
)

CREATE TABLE daily_system_metrics (
    date DATE PRIMARY KEY,
    total_precipitation_m3 NUMERIC,
    total_occupancy_m3 NUMERIC,
    total_capacity_m3 NUMERIC,
    system_occupancy_pct NUMERIC,
    total_consumption_m3 NUMERIC,
    net_change_m3 NUMERIC
);


ALTER TABLE city_consumption
ADD CONSTRAINT unique_city_date UNIQUE (city_name, date);