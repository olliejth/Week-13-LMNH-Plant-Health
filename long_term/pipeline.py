"""Full pipleine to extract data from an AWS RDS and uplaod it to an S3 bucket."""

from long_term.load_long import load_recordings


def main() -> None:
    """Main function, calls ETL functions individually."""

    # CHANGE when extract script is completed
    # data = extract_function()

    # CHANGE when transform script completed
    # dataframe = transform_function(data)

    load_recordings(dataframe)


if __name__ == "__main__":

    main()