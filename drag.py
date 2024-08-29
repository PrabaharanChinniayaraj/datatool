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





st.title("Conditional Filtering Widget for DataFrame")

def apply_condition(column, condition, value):
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
    mask = apply_condition(column, condition, value)
    filtered_df = df[mask]

    st.subheader("Filtered DataFrame")
    st.write(filtered_df)
st.title("DataFrame Aggregation Example")
st.write("Original DataFrame:")
st.dataframe(df)

# Select columns for aggregation
default_columns = ["", ""]
available_defaults = [col for col in default_columns if col in df.columns]

# Select columns for grouping
group_columns = st.multiselect("Select columns to group by", options=df.columns.tolist(), default=available_defaults)

# Select aggregate functions
aggregate_functions = {
    "Sum": "sum",
    "Mean": "mean",
    "Max": "max",
    "Min": "min",
    "Count": "count"
}

selected_aggregates = st.multiselect("Select aggregate functions", options=list(aggregate_functions.keys()), default=["Sum", "Mean"])

# Apply group by and aggregate functions
if group_columns and selected_aggregates:
    agg_dict = {col: [aggregate_functions[func] for func in selected_aggregates] for col in df.columns if col not in group_columns}
    grouped_df = df.groupby(group_columns).agg(agg_dict)
    grouped_df.columns = ['_'.join(col) for col in grouped_df.columns]

    st.subheader("Grouped and Aggregated Data")
    st.write(grouped_df)

# Example: Save the grouped data to a CSV file
if st.button("Save to CSV"):
    grouped_df.to_csv("grouped_data.csv")
    st.write("Data saved to grouped_data.csv")
