import pandas as pd
import numpy as np


def dataset_overview(df):

    insights = []

    insights.append(f"Dataset contains {df.shape[0]} rows and {df.shape[1]} columns.")

    insights.append(
        f"There are {df.isnull().sum().sum()} missing values in the dataset."
    )

    insights.append(
        f"There are {df.duplicated().sum()} duplicate rows."
    )

    return insights


def missing_value_insights(df):

    insights = []

    missing = df.isnull().sum()

    for column, value in missing.items():

        if value > 0:

            percentage = round((value / len(df)) * 100, 2)

            insights.append(
                f"{column} has {value} missing values ({percentage}%)."
            )

    if not insights:

        insights.append("No missing values found.")

    return insights


def duplicate_insights(df):

    duplicates = df.duplicated().sum()

    if duplicates == 0:
        return ["No duplicate rows found."]

    return [f"{duplicates} duplicate rows detected."]


def numeric_column_insights(df):

    insights = []

    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.empty:

        return ["No numerical columns available."]

    for column in numeric_df.columns:

        insights.append(
            f"{column}: Mean={round(df[column].mean(),2)}, Min={df[column].min()}, Max={df[column].max()}"
        )

    return insights


def categorical_column_insights(df):

    insights = []

    categorical_df = df.select_dtypes(exclude=np.number)

    if categorical_df.empty:

        return ["No categorical columns available."]

    for column in categorical_df.columns:

        top = df[column].mode()[0]

        count = df[column].value_counts().iloc[0]

        insights.append(
            f"Most frequent value in '{column}' is '{top}' ({count} occurrences)."
        )

    return insights


def outlier_insights(df):

    insights = []

    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.empty:

        return ["No numerical columns available."]

    for column in numeric_df.columns:

        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - (1.5 * iqr)
        upper = q3 + (1.5 * iqr)

        outliers = df[
            (df[column] < lower) |
            (df[column] > upper)
        ]

        insights.append(
            f"{column} contains {len(outliers)} potential outliers."
        )

    return insights


def recommendation_engine(df):

    recommendations = []

    if df.isnull().sum().sum() > 0:

        recommendations.append(
            "Fill missing values before performing analysis."
        )

    if df.duplicated().sum() > 0:

        recommendations.append(
            "Remove duplicate rows."
        )

    numeric = df.select_dtypes(include=np.number)

    if len(numeric.columns) >= 2:

        recommendations.append(
            "Use a Correlation Heatmap to understand relationships."
        )

        recommendations.append(
            "Visualize numerical columns using Scatter Plot."
        )

    categorical = df.select_dtypes(exclude=np.number)

    if len(categorical.columns) > 0:

        recommendations.append(
            "Use Bar Chart or Pie Chart for categorical columns."
        )

    recommendations.append(
        "Generate Summary Statistics before building any ML model."
    )

    return recommendations


def generate_ai_insights(df):

    return {
        "Dataset Overview": dataset_overview(df),
        "Missing Value Insights": missing_value_insights(df),
        "Duplicate Insights": duplicate_insights(df),
        "Numerical Insights": numeric_column_insights(df),
        "Categorical Insights": categorical_column_insights(df),
        "Outlier Insights": outlier_insights(df),
        "Recommendations": recommendation_engine(df)
    }