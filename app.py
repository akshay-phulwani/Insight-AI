import os
from datetime import datetime

import pandas as pd
import streamlit as st

from analytics.analysis import (
    categorical_columns,
    categorical_summary,
    correlation_matrix,
    data_types,
    dataset_overview,
    dataset_shape,
    full_summary,
    memory_usage,
    missing_values,
    numerical_columns,
    numeric_summary,
    summary_statistics,
    unique_values,
)
from analytics.cleaning import (
    dataset_summary,
    drop_missing_values,
    fill_missing_values,
    remove_duplicates,
)
from analytics.insights import generate_ai_insights
from analytics.visualization import (
    area_chart,
    bar_chart,
    box_plot,
    correlation_heatmap,
    create_dashboard_kpis,
    funnel_chart,
    histogram,
    line_chart,
    pie_chart,
    scatter_plot,
    sunburst_chart,
    treemap_chart,
)
from database.queries import insert_dataset
from reports.report_generator import generate_pdf_report


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
REPORT_FOLDER = os.path.join(BASE_DIR, "reports", "generated")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

st.set_page_config(
    page_title="InsightAI",
    page_icon=":bar_chart:",
    layout="wide",
)


def initialize_state():
    defaults = {
        "df": None,
        "file_name": None,
        "file_path": None,
        "metadata_saved_for": None,
        "report_path": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def show_kpis(df):
    kpis = create_dashboard_kpis(df)
    columns = st.columns(4)

    columns[0].metric("Rows", kpis["Rows"])
    columns[1].metric("Columns", kpis["Columns"])
    columns[2].metric("Missing Values", kpis["Missing Values"])
    columns[3].metric("Duplicate Rows", kpis["Duplicate Rows"])


def require_dataset():
    if st.session_state.df is None:
        st.warning("Please upload a dataset first.")
        return None

    return st.session_state.df


def read_uploaded_file(uploaded_file, save_path):
    if uploaded_file.name.lower().endswith(".csv"):
        return pd.read_csv(save_path)

    return pd.read_excel(save_path)


def save_metadata_once(file_name, df):
    metadata_key = (file_name, df.shape[0], df.shape[1])

    if st.session_state.metadata_saved_for == metadata_key:
        return

    try:
        insert_dataset(
            file_name,
            file_name.split(".")[-1],
            df.shape[0],
            df.shape[1],
        )
        st.session_state.metadata_saved_for = metadata_key
    except Exception as exc:
        st.warning(f"Dataset loaded, but metadata could not be saved: {exc}")


def reset_dataset(remove_file=False):
    if (
        remove_file
        and st.session_state.file_path
        and os.path.exists(st.session_state.file_path)
    ):
        os.remove(st.session_state.file_path)

    st.session_state.df = None
    st.session_state.file_name = None
    st.session_state.file_path = None
    st.session_state.metadata_saved_for = None
    st.session_state.report_path = None


def render_insight_list(items):
    for item in items:
        st.write(f"- {item}")


def choose_default(options, preferred):
    if preferred in options:
        return options.index(preferred)

    return 0


initialize_state()

st.sidebar.title("InsightAI")
page = st.sidebar.radio(
    "Navigation",
    [
        "Upload Dataset",
        "Data Cleaning",
        "Analytics",
        "Visualization",
        "AI Insights",
        "Reports",
    ],
)

if page == "Upload Dataset":
    st.title("Upload Dataset")
    st.caption("Upload a CSV or Excel file to begin the analytics workflow.")

    if st.session_state.df is not None:
        df = st.session_state.df

        st.success(f"Current dataset: {st.session_state.file_name}")
        show_kpis(df)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Upload Another Dataset", use_container_width=True):
                reset_dataset()
                st.rerun()

        with col2:
            if st.button("Remove Dataset", use_container_width=True):
                try:
                    reset_dataset(remove_file=True)
                    st.success("Dataset removed.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not remove dataset: {exc}")

        st.divider()

        with st.expander("Dataset Information", expanded=True):
            shape = dataset_shape(df)
            c1, c2, c3 = st.columns(3)
            c1.metric("Shape", f"{shape['Rows']} x {shape['Columns']}")
            c2.metric("Memory", f"{memory_usage(df)} MB")
            c3.metric("Unique Columns", len(df.columns))

        with st.expander("Data Types", expanded=True):
            st.dataframe(data_types(df), use_container_width=True)

        with st.expander("Dataset Preview", expanded=True):
            st.dataframe(df.head(20), use_container_width=True)

    else:
        uploaded_file = st.file_uploader(
            "Choose CSV or Excel",
            type=["csv", "xlsx", "xls"],
        )

        if uploaded_file is not None:
            try:
                save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

                with st.spinner("Uploading and reading dataset..."):
                    with open(save_path, "wb") as file:
                        file.write(uploaded_file.getbuffer())

                    df = read_uploaded_file(uploaded_file, save_path)

                st.session_state.df = df
                st.session_state.file_name = uploaded_file.name
                st.session_state.file_path = save_path
                save_metadata_once(uploaded_file.name, df)

                st.success("Dataset uploaded successfully.")
                st.rerun()
            except Exception as exc:
                st.error(f"Could not upload dataset: {exc}")

elif page == "Data Cleaning":
    st.title("Data Cleaning")
    df = require_dataset()

    if df is not None:
        try:
            summary = dataset_summary(df)
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Rows", summary["Rows"])
            col2.metric("Columns", summary["Columns"])
            col3.metric("Missing Values", summary["Missing Values"])
            col4.metric("Duplicate Rows", summary["Duplicate Rows"])

            st.divider()

            c1, c2, c3 = st.columns(3)

            with c1:
                if st.button("Remove Duplicates", use_container_width=True):
                    st.session_state.df = remove_duplicates(df)
                    st.success("Duplicate rows removed.")
                    st.rerun()

            with c2:
                if st.button("Fill Missing Values", use_container_width=True):
                    st.session_state.df = fill_missing_values(df)
                    st.success("Missing values filled.")
                    st.rerun()

            with c3:
                if st.button("Drop Missing Values", use_container_width=True):
                    st.session_state.df = drop_missing_values(df)
                    st.success("Rows with missing values dropped.")
                    st.rerun()

            st.divider()
            st.subheader("Cleaned Dataset")
            st.dataframe(st.session_state.df, use_container_width=True)

            csv = st.session_state.df.to_csv(index=False)
            st.download_button(
                label="Download Clean Dataset",
                data=csv,
                file_name="clean_dataset.csv",
                mime="text/csv",
            )
        except Exception as exc:
            st.error(f"Cleaning failed: {exc}")

elif page == "Analytics":
    st.title("Analytics")
    df = require_dataset()

    if df is not None:
        try:
            overview = dataset_overview(df)
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Rows", overview["Rows"])
            col2.metric("Columns", overview["Columns"])
            col3.metric("Missing Values", overview["Missing Values"])
            col4.metric("Duplicate Rows", overview["Duplicate Rows"])
            col5.metric("Memory", f"{overview['Memory Usage (MB)']} MB")

            st.divider()

            with st.expander("Dataset Overview", expanded=True):
                st.json(overview)

            with st.expander("Summary Statistics", expanded=True):
                st.dataframe(full_summary(df), use_container_width=True)

            with st.expander("Numerical Summary"):
                numeric = numeric_summary(df)
                if numeric.empty:
                    st.info("No numerical columns available.")
                else:
                    st.dataframe(numeric, use_container_width=True)

            with st.expander("Categorical Summary"):
                categorical = categorical_summary(df)
                if categorical.empty:
                    st.info("No categorical columns available.")
                else:
                    st.dataframe(categorical, use_container_width=True)

            with st.expander("Missing Values Table"):
                st.dataframe(missing_values(df), use_container_width=True)

            with st.expander("Data Types"):
                st.dataframe(data_types(df), use_container_width=True)

            with st.expander("Correlation Matrix"):
                corr = correlation_matrix(df)
                if corr.empty:
                    st.info("At least two numerical columns are required.")
                else:
                    st.dataframe(corr, use_container_width=True)

            with st.expander("Memory Usage and Shape"):
                shape = dataset_shape(df)
                st.write(f"Dataset shape: {shape['Rows']} rows x {shape['Columns']} columns")
                st.write(f"Memory usage: {memory_usage(df)} MB")

            with st.expander("Unique Values"):
                st.dataframe(unique_values(df), use_container_width=True)

            with st.expander("Numeric Describe"):
                numeric_stats = summary_statistics(df)
                st.dataframe(numeric_stats, use_container_width=True)
        except Exception as exc:
            st.error(f"Analytics failed: {exc}")

elif page == "Visualization":
    st.title("Visualization")
    df = require_dataset()

    if df is not None:
        try:
            show_kpis(df)
            st.divider()

            numeric_cols = numerical_columns(df)
            categorical_cols = categorical_columns(df)
            all_cols = df.columns.tolist()

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Bar Chart",
                    "Line Chart",
                    "Pie Chart",
                    "Histogram",
                    "Scatter Plot",
                    "Box Plot",
                    "Correlation Heatmap",
                    "Area Chart",
                    "Treemap",
                    "Sunburst",
                    "Funnel Chart",
                ],
            )

            fig = None

            with st.spinner("Generating chart..."):
                if chart_type in ["Bar Chart", "Line Chart", "Area Chart", "Funnel Chart"]:
                    default_x = categorical_cols[0] if categorical_cols else all_cols[0]
                    default_y = numeric_cols[0] if numeric_cols else all_cols[0]
                    c1, c2 = st.columns(2)
                    x_column = c1.selectbox(
                        "X Column",
                        all_cols,
                        index=choose_default(all_cols, default_x),
                    )
                    y_column = c2.selectbox(
                        "Y Column",
                        all_cols,
                        index=choose_default(all_cols, default_y),
                    )

                    if chart_type == "Bar Chart":
                        fig = bar_chart(df, x_column, y_column)
                    elif chart_type == "Line Chart":
                        fig = line_chart(df, x_column, y_column)
                    elif chart_type == "Area Chart":
                        fig = area_chart(df, x_column, y_column)
                    else:
                        fig = funnel_chart(df, x_column, y_column)

                elif chart_type == "Pie Chart":
                    if not numeric_cols:
                        st.warning("Pie charts require at least one numerical values column.")
                    else:
                        default_names = categorical_cols[0] if categorical_cols else all_cols[0]
                        c1, c2 = st.columns(2)
                        names_column = c1.selectbox(
                            "Names Column",
                            all_cols,
                            index=choose_default(all_cols, default_names),
                        )
                        values_column = c2.selectbox("Values Column", numeric_cols)
                        fig = pie_chart(df, names_column, values_column)

                elif chart_type == "Histogram":
                    if not numeric_cols:
                        st.warning("Histograms require at least one numerical column.")
                    else:
                        column = st.selectbox("Column", numeric_cols)
                        fig = histogram(df, column)

                elif chart_type == "Scatter Plot":
                    if len(numeric_cols) < 2:
                        st.warning("Scatter plots require at least two numerical columns.")
                    else:
                        c1, c2 = st.columns(2)
                        x_column = c1.selectbox("X Column", numeric_cols)
                        y_column = c2.selectbox("Y Column", numeric_cols, index=1)
                        fig = scatter_plot(df, x_column, y_column)

                elif chart_type == "Box Plot":
                    if not numeric_cols:
                        st.warning("Box plots require at least one numerical column.")
                    else:
                        column = st.selectbox("Column", numeric_cols)
                        fig = box_plot(df, column)

                elif chart_type == "Correlation Heatmap":
                    if len(numeric_cols) < 2:
                        st.warning("Correlation heatmaps require at least two numerical columns.")
                    else:
                        fig = correlation_heatmap(df)

                elif chart_type in ["Treemap", "Sunburst"]:
                    if not categorical_cols or not numeric_cols:
                        st.warning(f"{chart_type} requires categorical path columns and a numerical values column.")
                    else:
                        path_columns = st.multiselect(
                            "Path Columns",
                            categorical_cols,
                            default=categorical_cols[: min(2, len(categorical_cols))],
                        )
                        values_column = st.selectbox("Values Column", numeric_cols)

                        if path_columns:
                            if chart_type == "Treemap":
                                fig = treemap_chart(df, path_columns, values_column)
                            else:
                                fig = sunburst_chart(df, path_columns, values_column)
                        else:
                            st.warning("Select at least one path column.")

            if fig is not None:
                st.plotly_chart(fig, use_container_width=True)
        except Exception as exc:
            st.error(f"Chart generation failed: {exc}")

elif page == "AI Insights":
    st.title("AI Insights")
    df = require_dataset()

    if df is not None:
        try:
            show_kpis(df)
            st.divider()

            with st.spinner("Generating insights..."):
                insights = generate_ai_insights(df)

            st.subheader("AI Analytics Assistant")
            st.caption("A rule-based assistant summary generated from the current dataset.")

            for section, items in insights.items():
                with st.expander(section, expanded=section in ["Dataset Overview", "Recommendations"]):
                    render_insight_list(items)
        except Exception as exc:
            st.error(f"Insight generation failed: {exc}")

elif page == "Reports":
    st.title("Reports")
    df = require_dataset()

    if df is not None:
        try:
            show_kpis(df)
            st.divider()

            st.write("Generate a PDF report from the current dataset, analytics, and AI insights.")

            if st.button("Generate Report", type="primary"):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                report_path = os.path.join(
                    REPORT_FOLDER,
                    f"InsightAI_Report_{timestamp}.pdf",
                )

                with st.spinner("Generating PDF report..."):
                    insights = generate_ai_insights(df)
                    st.session_state.report_path = generate_pdf_report(
                        df=df,
                        output_path=report_path,
                        insights=insights,
                        dataset_name=st.session_state.file_name or "Dataset",
                    )

                st.success("Report generated successfully.")

            if st.session_state.report_path and os.path.exists(st.session_state.report_path):
                with open(st.session_state.report_path, "rb") as file:
                    st.download_button(
                        "Download Report",
                        data=file,
                        file_name=os.path.basename(st.session_state.report_path),
                        mime="application/pdf",
                    )
        except Exception as exc:
            st.error(f"Report generation failed: {exc}")
