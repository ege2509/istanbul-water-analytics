CREATE TABLE dams (
id SERIAL PRIMARY KEY,
    dam_name VARCHAR(50) NOT NULL UNIQUE,
    max_capacity_m3 DECIMAL(12, 2) NOT NULL
)

CREATE TABLE daily_dam (
id SERIAL PRIMARY KEY,
    dam_id INTEGER NOT NULL REFERENCES dams(id),
	percipitation_pct DECIMAL(5, 2),
	percipitation_m3 DECIMAL(12,2),
	occupancy_pct DECIMAL(5,2),
	occupancy_m3 DECIMAL(12,2),
	date DATE
)

CREATE TABLE city_consumption (
id SERIAL PRIMARY KEY,
city_name TEXT,
consumption_m3 INTEGER
)