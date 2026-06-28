import pandas as pd


def dataset_summary(df):

    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": df.isnull().sum().sum(),
        "Duplicate Rows": df.duplicated().sum()
    }


def get_missing_values(df):

    missing = df.isnull().sum()

    return missing[missing > 0]


def get_duplicate_rows(df):

    return df[df.duplicated()]


def remove_duplicates(df):

    cleaned_df = df.drop_duplicates()

    return cleaned_df


def fill_missing_values(df):

    cleaned_df = df.copy()

    numeric_columns = cleaned_df.select_dtypes(include=["number"]).columns

    for column in numeric_columns:
        cleaned_df[column] = cleaned_df[column].fillna(
            cleaned_df[column].mean()
        )

    categorical_columns = cleaned_df.select_dtypes(include=["object"]).columns

    for column in categorical_columns:

        if not cleaned_df[column].mode().empty:

            cleaned_df[column] = cleaned_df[column].fillna(
                cleaned_df[column].mode()[0]
            )

    return cleaned_df


def drop_missing_values(df):

    return df.dropna()


def convert_data_types(df):

    cleaned_df = df.copy()

    for column in cleaned_df.columns:

        try:
            cleaned_df[column] = pd.to_numeric(cleaned_df[column])
        except:
            pass

    return cleaned_df


def remove_empty_columns(df):

    return df.dropna(axis=1, how="all")


def remove_empty_rows(df):

    return df.dropna(axis=0, how="all")


def clean_dataset(df):

    cleaned_df = df.copy()

    cleaned_df = remove_duplicates(cleaned_df)

    cleaned_df = fill_missing_values(cleaned_df)

    cleaned_df = remove_empty_columns(cleaned_df)

    cleaned_df = remove_empty_rows(cleaned_df)

    cleaned_df = convert_data_types(cleaned_df)

    return cleaned_df