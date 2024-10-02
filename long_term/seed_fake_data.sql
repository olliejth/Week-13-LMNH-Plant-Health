-- Seeding the database with more dummy data

-- Insert into botanist
INSERT INTO beta.botanist (first_name, last_name, email, phone) VALUES
('Alice', 'Smith', 'alice.smith@example.com', '123-456-7890'),
('Bob', 'Johnson', 'bob.johnson@example.com', '234-567-8901'),
('Charlie', 'Brown', 'charlie.brown@example.com', '345-678-9012'),
('Diana', 'Prince', 'diana.prince@example.com', '456-789-0123'),
('Ethan', 'Hunt', 'ethan.hunt@example.com', '567-890-1234'),
('Fiona', 'Green', 'fiona.green@example.com', '678-901-2345'),
('George', 'Martin', 'george.martin@example.com', '789-012-3456'),
('Hannah', 'Montana', 'hannah.montana@example.com', '890-123-4567'),
('Ian', 'Curtis', 'ian.curtis@example.com', '901-234-5678'),
('Julia', 'Roberts', 'julia.roberts@example.com', '012-345-6789');

-- Insert into origin_location
INSERT INTO beta.origin_location (latitude, longitude, town, timezone) VALUES
(51.5074, -0.1278, 'London', 'GMT'),
(40.7128, -74.0060, 'New York', 'EST'),
(34.0522, -118.2437, 'Los Angeles', 'PST'),
(48.8566, 2.3522, 'Paris', 'CET'),
(35.6895, 139.6917, 'Tokyo', 'JST'),
(55.7558, 37.6173, 'Moscow', 'MSK'),
(-33.4489, -70.6693, 'Santiago', 'CLT'),
(-34.6037, -58.3816, 'Buenos Aires', 'ART'),
(1.3521, 103.8198, 'Singapore', 'SGT'),
(52.5200, 13.4050, 'Berlin', 'CET');

-- Insert into plant
INSERT INTO beta.plant (plant_id, plant_name, plant_scientific_name, origin_location_id, small_url, medium_url, original_url, regular_url, thumbnail_url) VALUES
(1, 'Rose', 'Rosa rubiginosa', 1, 'http://example.com/rose_small.jpg', 'http://example.com/rose_medium.jpg', 'http://example.com/rose_original.jpg', 'http://example.com/rose_regular.jpg', 'http://example.com/rose_thumbnail.jpg'),
(2, 'Sunflower', 'Helianthus annuus', 2, 'http://example.com/sunflower_small.jpg', 'http://example.com/sunflower_medium.jpg', 'http://example.com/sunflower_original.jpg', 'http://example.com/sunflower_regular.jpg', 'http://example.com/sunflower_thumbnail.jpg'),
(3, 'Tulip', 'Tulipa', 3, 'http://example.com/tulip_small.jpg', 'http://example.com/tulip_medium.jpg', 'http://example.com/tulip_original.jpg', 'http://example.com/tulip_regular.jpg', 'http://example.com/tulip_thumbnail.jpg'),
(4, 'Daisy', 'Bellis perennis', 4, 'http://example.com/daisy_small.jpg', 'http://example.com/daisy_medium.jpg', 'http://example.com/daisy_original.jpg', 'http://example.com/daisy_regular.jpg', 'http://example.com/daisy_thumbnail.jpg'),
(5, 'Orchid', 'Orchidaceae', 5, 'http://example.com/orchid_small.jpg', 'http://example.com/orchid_medium.jpg', 'http://example.com/orchid_original.jpg', 'http://example.com/orchid_regular.jpg', 'http://example.com/orchid_thumbnail.jpg'),
(6, 'Cactus', 'Cactaceae', 6, 'http://example.com/cactus_small.jpg', 'http://example.com/cactus_medium.jpg', 'http://example.com/cactus_original.jpg', 'http://example.com/cactus_regular.jpg', 'http://example.com/cactus_thumbnail.jpg'),
(7, 'Fern', 'Pteridophyta', 7, 'http://example.com/fern_small.jpg', 'http://example.com/fern_medium.jpg', 'http://example.com/fern_original.jpg', 'http://example.com/fern_regular.jpg', 'http://example.com/fern_thumbnail.jpg'),
(8, 'Bamboo', 'Bambusoideae', 8, 'http://example.com/bamboo_small.jpg', 'http://example.com/bamboo_medium.jpg', 'http://example.com/bamboo_original.jpg', 'http://example.com/bamboo_regular.jpg', 'http://example.com/bamboo_thumbnail.jpg'),
(9, 'Lavender', 'Lavandula', 9, 'http://example.com/lavender_small.jpg', 'http://example.com/lavender_medium.jpg', 'http://example.com/lavender_original.jpg', 'http://example.com/lavender_regular.jpg', 'http://example.com/lavender_thumbnail.jpg'),
(10, 'Mint', 'Mentha', 10, 'http://example.com/mint_small.jpg', 'http://example.com/mint_medium.jpg', 'http://example.com/mint_original.jpg', 'http://example.com/mint_regular.jpg', 'http://example.com/mint_thumbnail.jpg');

-- Seeding the reading table with dummy data for the last 3 days
DECLARE @startTime DATETIME = DATEADD(DAY, -3, GETDATE()); -- Starting point for readings
DECLARE @endTime DATETIME = GETDATE(); -- Current time
DECLARE @readingCount INT = DATEDIFF(MINUTE, @startTime, @endTime) + 1; -- Total readings

-- Loop through each plant and botanist to create readings every minute
DECLARE @plant_id SMALLINT;
DECLARE @botanist_id SMALLINT;
DECLARE @i INT;

SET @i = 0;

WHILE @i < @readingCount
BEGIN
    SET @plant_id = (1 + (@i % 10)); -- Rotate through 10 plants
    SET @botanist_id = (1 + (@i % 10)); -- Rotate through 10 botanists

    INSERT INTO beta.reading (plant_id, botanist_id, at, last_watered, soil_moisture, temperature) VALUES
    (@plant_id, @botanist_id, DATEADD(MINUTE, @i, @startTime), DATEADD(DAY, -2, DATEADD(MINUTE, @i, @startTime)), 
     CAST(RAND() * 100 AS DECIMAL(5, 2)), -- Random soil moisture between 0 and 100
     CAST(RAND() * 40 AS DECIMAL(5, 2)) + 15); -- Random temperature between 15 and 55

    SET @i = @i + 1; -- Increment to the next minute
END
