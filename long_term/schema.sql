-- SQL to initialise database.

DROP TABLE IF EXISTS reading;
DROP TABLE IF EXISTS plant;
DROP TABLE IF EXISTS origin_location;
DROP TABLE IF EXISTS botanist;

CREATE TABLE botanist(
    botanist_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    PRIMARY KEY botanist_id
);

CREATE TABLE origin_location(
    location_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    latitude DECIMAL(11,8) NOT NULL,
    longitude DECIMAL(11,8) NOT NULL,
    town VARCHAR(255) NOT NULL,
    timezone VARCHAR(255) NOT NULL,
    PRIMARY KEY location_id
);

