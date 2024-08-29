import streamlit as st
from streamlit_sortables import sort_items
import pandas as pd


def change_case(df, column, case_type):
    if case_type == "lowercase":
        df[column] = df[column].str.lower()
    elif case_type == "uppercase":
        df[column] = df[column].str.upper()
    elif case_type == "sentence case":
        df[column] = df[column].str.capitalize()
    return df

def apply_condition(df, column, condition, value):
    if condition == "equals":
        return df[column] == value
    elif condition == "not equals":
        return df[column] != value
    elif condition == "greater than":
        return df[column] > value
    elif condition == "less than":
        return df[column] < value
    elif condition == "greater than or equal":
        return df[column] >= value
    elif condition == "less than or equal":
        return df[column] <= value
    elif condition == "contains":
        return df[column].str.contains(value, case=False, na=False)
    elif condition == "does not contain":
        return ~df[column].str.contains(value, case=False, na=False)

st.title("Draggable Date Format Widget")
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Load the Excel file
    xls = pd.ExcelFile(uploaded_file)
    
    # Display the available sheets
    sheet_names = xls.sheet_names
    sheet_choice = st.selectbox("Select a sheet", sheet_names)
    
    # Input box to enter the number of rows to skip
    skip_rows = st.number_input("Number of rows to skip", min_value=0, value=0, step=1)
    
    # Load the selected sheet with the specified number of rows to skip
    if sheet_choice:
        df = pd.read_excel(xls, sheet_name=sheet_choice, skiprows=skip_rows)
        
        # Display the dataframe
        st.write(f"Displaying data from '{sheet_choice}' with {skip_rows} rows skipped:")
        st.dataframe(df)
        
        # Change case feature
        column = st.selectbox("Select a column to change case:", df.columns)
        case_type = st.radio("Select case type:", ("lowercase", "uppercase", "sentence case"))

        if st.button("Change Case"):
            df = change_case(df, column, case_type)
            st.write("Updated Data:")
            st.dataframe(df)

        # List of date format components
        date_components = ["Day", "Month", "Year"]

        # Display the draggable list
        st.subheader("Created By-: Prabaharan Chinniayaraju")
        st.subheader("Drag and Drop to Create Your Date Format")
        sorted_date_components = sort_items(date_components, direction="horizontal", key="date_format")

        # Display the selected date format
        st.subheader("Selected Date Format")
        formatted_date = "-".join(sorted_date_components)
        st.write(f"Date Format: {formatted_date}")

        # Optional: Display an example date using the selected format
        example_date = {"Day": "12", "Month": "08", "Year": "2024"}
        formatted_example_date = "-".join([example_date[component] for component in sorted_date_components])
        st.write(f"Example: {formatted_example_date}")

        # Conditional Filtering Widget for DataFrame
        st.title("Conditional Filtering Widget for DataFrame")

        column = st.selectbox("Select column to filter", df.columns)
        if df[column].dtype in ['int64', 'float64']:
            condition = st.selectbox("Select condition", ["equals", "not equals", "greater than", "less than", "greater than or equal", "less than or equal"])
            value = st.number_input(f"Enter value for {column}")
        elif df[column].dtype == 'object':
            condition = st.selectbox("Select condition", ["equals", "not equals", "contains", "does not contain"])
            value = st.text_input(f"Enter value for {column}")
        else:
            st.write(f"Filtering not supported for column type: {df[column].dtype}")
            condition, value = None, None

        if condition and value is not None:
            mask = apply_condition(df, column, condition, value)
            filtered_df = df[mask]

            st.subheader("Filtered DataFrame")
            st.write(filtered_df)

        # DataFrame Aggregation Example
        st.title("DataFrame Aggregation Example")
        st.write("Original DataFrame:")
        st.dataframe(df)

        group_by_columns = st.multiselect("Select columns to group by", df.columns)

        # Select columns to aggregate
        aggregate_columns = st.multiselect("Select columns to aggregate", df.columns)

        # Select aggregate functions
        agg_functions = st.multiselect("Select aggregate functions", ["sum", "mean", "min", "max", "count"])

        # Apply the aggregation
        if st.button("Aggregate"):
            if group_by_columns and aggregate_columns and agg_functions:
                agg_dict = {col: agg_functions for col in aggregate_columns}
                aggregated_df = df.groupby(group_by_columns).agg(agg_dict)
                st.write("Aggregated DataFrame:")
                st.dataframe(aggregated_df)
            else:
                st.write("Please select columns and aggregate functions.")
