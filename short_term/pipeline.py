"""Whole pipeline script for short-term storage."""

from os import environ as ENV
from dotenv import load_dotenv

from extract import extract_recordings
from load import load_recordings


def main(env: dict) -> None:
    """Extracts and uploads API data to S3."""
    file_name = extract_recordings()
    load_recordings(env, file_name)


if __name__ == "__main__":

    load_dotenv()

    main(ENV)
