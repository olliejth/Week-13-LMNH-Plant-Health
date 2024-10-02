-- SQL to initialise the database for Microsoft SQL Server.

IF OBJECT_ID('beta.reading', 'U') IS NOT NULL DROP TABLE beta.reading;
IF OBJECT_ID('beta.plant', 'U') IS NOT NULL DROP TABLE beta.plant;
IF OBJECT_ID('beta.origin_location', 'U') IS NOT NULL DROP TABLE beta.origin_location;
IF OBJECT_ID('beta.botanist', 'U') IS NOT NULL DROP TABLE beta.botanist;

CREATE TABLE beta.botanist(
    botanist_id SMALLINT IDENTITY(1,1),
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY(botanist_id)
);

CREATE TABLE beta.origin_location(
    location_id SMALLINT IDENTITY(1,1),
    latitude DECIMAL(11,8) NOT NULL,
    longitude DECIMAL(11,8) NOT NULL,
    town VARCHAR(255) NOT NULL,
    timezone VARCHAR(50) NOT NULL,
    PRIMARY KEY (location_id),
    CONSTRAINT unique_location_combination UNIQUE (latitude, longitude, town, timezone)
);

CREATE TABLE beta.plant(
    plant_id SMALLINT NOT NULL,
    plant_name VARCHAR(255) NOT NULL,
    plant_scientific_name VARCHAR(255) NULL UNIQUE,
    origin_location_id SMALLINT NOT NULL,
    -- Image URL fields are nullable
    small_url VARCHAR(MAX) NULL,
    medium_url VARCHAR(MAX) NULL,
    original_url VARCHAR(MAX) NULL,
    regular_url VARCHAR(MAX) NULL,
    thumbnail_url VARCHAR(MAX) NULL,
    PRIMARY KEY (plant_id),
    FOREIGN KEY (origin_location_id) REFERENCES beta.origin_location(location_id)
);

CREATE TABLE beta.reading(
    reading_id INT IDENTITY(1,1),
    plant_id SMALLINT NOT NULL,
    botanist_id SMALLINT NOT NULL,
    at DATETIME2 NOT NULL,
    last_watered DATETIME2 NOT NULL,
    soil_moisture DECIMAL(5,2) NOT NULL,
    temperature DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (reading_id),
    FOREIGN KEY (plant_id) REFERENCES beta.plant(plant_id),
    FOREIGN KEY (botanist_id) REFERENCES beta.botanist(botanist_id),
    CHECK (at <= SYSDATETIME()),
    CHECK (last_watered <= SYSDATETIME())
);
