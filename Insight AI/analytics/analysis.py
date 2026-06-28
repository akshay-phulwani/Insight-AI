import pandas as pd
import numpy as np


def dataset_shape(df):

    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1]
    }


def numerical_columns(df):

    return df.select_dtypes(include=np.number).columns.tolist()


def categorical_columns(df):

    return df.select_dtypes(exclude=np.number).columns.tolist()


def summary_statistics(df):

    return df.describe()


def full_summary(df):

    return df.describe(include="all")


def correlation_matrix(df):

    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.empty:
        return pd.DataFrame()

    return numeric_df.corr()


def missing_values(df):

    missing = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum(),
        "Percentage": (
            df.isnull().sum() / len(df) * 100
        ).round(2)
    })

    return missing.sort_values(
        by="Missing Values",
        ascending=False
    )


def unique_values(df):

    return pd.DataFrame({
        "Column": df.columns,
        "Unique Values": df.nunique()
    })


def data_types(df):

    return pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str)
    })


def memory_usage(df):

    memory = df.memory_usage(deep=True).sum()

    return round(memory / (1024 * 1024), 2)


def numeric_summary(df):

    numeric = df.select_dtypes(include=np.number)

    if numeric.empty:
        return pd.DataFrame()

    return pd.DataFrame({
        "Mean": numeric.mean(),
        "Median": numeric.median(),
        "Minimum": numeric.min(),
        "Maximum": numeric.max(),
        "Standard Deviation": numeric.std(),
        "Variance": numeric.var()
    })


def categorical_summary(df):

    categorical = df.select_dtypes(exclude=np.number)

    if categorical.empty:
        return pd.DataFrame()

    summary = pd.DataFrame(index=categorical.columns)

    summary["Unique"] = categorical.nunique()

    summary["Most Frequent"] = categorical.mode().iloc[0]

    summary["Frequency"] = [
        categorical[col].value_counts().iloc[0]
        for col in categorical.columns
    ]

    return summary


def dataset_overview(df):

    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum()),
        "Memory Usage (MB)": memory_usage(df)
    }