def generate_delta(df_reviews, df_previous_run):
    """
    Generating a delta Pandas DataFrame so as not to duplicate any data we have already gathered

    Args:
        - df_reviews (Pandas DataFrame): A DataFrame containing all the reviews of movies that Caelan has rated
        - df_previous_run (Pandas DataFrame): A DataFrame containing all the data from the previous run

    Returns:
        - df_reviews (Pandas DataFrame): A DataFrame containing only the reviews where we have not yet gathered the data
    """