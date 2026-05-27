SELECT
    city,
    temperature_category,
    COUNT(*) AS total_records,
    AVG(temperature) AS average_temperature
FROM
    `tokyo-crane-497603-t5.weather_pipeline.weather_data`
GROUP BY
    city, temperature_category
ORDER BY
    average_temperature DESC;