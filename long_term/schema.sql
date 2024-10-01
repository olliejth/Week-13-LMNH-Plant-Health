-- SQL to initialise database.

DROP TABLE IF EXISTS reading;
DROP TABLE IF EXISTS plant;
DROP TABLE IF EXISTS origin_location;
DROP TABLE IF EXISTS botanist;

CREATE TABLE botanist(
    botanist_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY(botanist_id)
);

CREATE TABLE origin_location(
    location_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    latitude DECIMAL(11,8) NOT NULL,
    longitude DECIMAL(11,8) NOT NULL,
    town VARCHAR(255) NOT NULL,
    timezone VARCHAR(50) NOT NULL,
    PRIMARY KEY (location_id),
     CONSTRAINT unique_location_combination UNIQUE (latitude, longitude, town, timezone)
);

CREATE TABLE plant(
    plant_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    plant_name VARCHAR(255) NOT NULL,
    plant_scientific_name VARCHAR(255) NULL UNIQUE,
    origin_location_id SMALLINT NOT NULL,
    -- Image URL fields are nullable
    small_url TEXT NULL,
    medium_url TEXT NULL,
    original_url TEXT NULL,
    regular_url TEXT NULL,
    thumbnail_url TEXT NULL,
    PRIMARY KEY (plant_id),
    FOREIGN KEY (origin_location_id) REFERENCES origin_location(location_id)
);

CREATE TABLE reading(
    reading_id INT GENERATED ALWAYS AS IDENTITY,
    plant_id SMALLINT NOT NULL,
    botanist_id SMALLINT NOT NULL,
    at TIMESTAMPTZ NOT NULL,
    last_watered TIMESTAMPTZ NOT NULL,
    soil_moisture DECIMAL(5,2) NOT NULL,
    temperature DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (reading_id),
    FOREIGN KEY (plant_id) REFERENCES plant(plant_id),
    FOREIGN KEY (botanist_id) REFERENCES botanist(botanist_id),
    CHECK (at <= NOW()),
    CHECK (last_watered <= NOW())
);