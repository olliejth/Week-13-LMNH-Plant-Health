"""Full pipeline to extract data from an AWS RDS and upload it to an S3 bucket."""

from extract_long import extract_readings
from transform_long import create_summary
from load_long import load_recordings


def long_term_etl() -> None:
    """Main function, calls ETL functions individually."""

    plants_df = extract_readings()

    cleaned_df = create_summary(plants_df)

    load_recordings(cleaned_df)


if __name__ == "__main__":

    long_term_etl()
