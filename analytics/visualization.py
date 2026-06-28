import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def bar_chart(df, x_column, y_column, title="Bar Chart"):

    fig = px.bar(
        df,
        x=x_column,
        y=y_column,
        title=title
    )

    return fig


def line_chart(df, x_column, y_column, title="Line Chart"):

    fig = px.line(
        df,
        x=x_column,
        y=y_column,
        title=title
    )

    return fig


def pie_chart(df, names_column, values_column, title="Pie Chart"):

    fig = px.pie(
        df,
        names=names_column,
        values=values_column,
        title=title
    )

    return fig


def histogram(df, column, title="Histogram"):

    fig = px.histogram(
        df,
        x=column,
        title=title
    )

    return fig


def scatter_plot(df, x_column, y_column, title="Scatter Plot"):

    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        title=title
    )

    return fig


def box_plot(df, column, title="Box Plot"):

    fig = px.box(
        df,
        y=column,
        title=title
    )

    return fig


def correlation_heatmap(df):

    numeric_df = df.select_dtypes(include=np.number)

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap"
    )

    return fig


def area_chart(df, x_column, y_column, title="Area Chart"):

    fig = px.area(
        df,
        x=x_column,
        y=y_column,
        title=title
    )

    return fig


def violin_plot(df, column, title="Violin Plot"):

    fig = px.violin(
        df,
        y=column,
        box=True,
        points="all",
        title=title
    )

    return fig


def density_heatmap(df, x_column, y_column, title="Density Heatmap"):

    fig = px.density_heatmap(
        df,
        x=x_column,
        y=y_column,
        title=title
    )

    return fig


def sunburst_chart(df, path_columns, values_column, title="Sunburst Chart"):

    fig = px.sunburst(
        df,
        path=path_columns,
        values=values_column,
        title=title
    )

    return fig


def treemap_chart(df, path_columns, values_column, title="Treemap"):

    fig = px.treemap(
        df,
        path=path_columns,
        values=values_column,
        title=title
    )

    return fig


def funnel_chart(df, x_column, y_column, title="Funnel Chart"):

    fig = px.funnel(
        df,
        x=x_column,
        y=y_column,
        title=title
    )

    return fig


def create_dashboard_kpis(df):

    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum())
    }