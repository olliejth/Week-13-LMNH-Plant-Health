# Week-13-LMNH-Plant-Health

# Project Overview

LNMH has an array of sensors setup to monitor the health of a plant but they are currently only configured with a single, simple API endpoint that reports the current health of a plant. The museum wants to be able to monitor the health of the plants over time and to be able to alert the gardeners when there is a problem. They will need to store the data in long term storage and be able to query the data to create visualisations and alerts.

# Project Aims

This project aims to build a robust pipeline to form an automated data analysis pipeline for the botanical gardens in the LMNH.

An interactive dashboard will be provided to offer insights into plant healtha over many key metrics over time.

# Technical Overview

## Short term pipeline (AWS Lambda - Runs minutely)
1. Asyncronously queries plant API endpoints.
2. Uploads plant readings to a Microsoft SQL server RDS instance.

## Long term pipeline (AWS Lambda - Runs daily)
1. Queries the past day's data from the RDS instance.
2. Analyses and processes the data, collecting key statistical metrics.
3. Uploads these metrics to an S3 data for long-term archived storage.

## Interactive Dashboard
- Pulls data from the RDS instance to provide key insights into plant health metrics.