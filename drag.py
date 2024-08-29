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





st.title("Draggable DataFrame Filter Widget")

# List of filter components (columns)
filter_columns =  df.columns

# Draggable list for selecting filter columns
st.subheader("Drag and Drop to Select Filter Columns")
sorted_columns = sort_items(filter_columns, direction="vertical", key="filter_columns")

# Display the filters for each selected column
st.subheader("Apply Filters")
filters = {}
for column in sorted_columns:
    if column == "Age" or column == "Score":
        min_val, max_val = st.slider(f"Select range for {column}", min_value=int(df[column].min()), max_value=int(df[column].max()), value=(int(df[column].min()), int(df[column].max())))
        filters[column] = (min_val, max_val)
    elif column == "City":
        selected_cities = st.multiselect(f"Select values for {column}", options=df[column].unique(), default=list(df[column].unique()))
        filters[column] = selected_cities

# Apply filters to the DataFrame
filtered_df = df.copy()
for column, condition in filters.items():
    if column in ["Age", "Score"]:
        filtered_df = filtered_df[(filtered_df[column] >= condition[0]) & (filtered_df[column] <= condition[1])]
    elif column == "City":
        filtered_df = filtered_df[filtered_df[column].isin(condition)]

# Display the filtered DataFrame
st.subheader("Filtered DataFrame")
st.write(filtered_df)


import streamlit as st
import pandas as pd

# Sample DataFrame
data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "Age": [24, 27, 22, 32, 29],
    "City": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
    "Score": [85, 91, 88, 95, 79]
}
df = pd.DataFrame(data)

st.title("Conditional Filtering Widget for DataFrame")

# Function to apply the selected condition
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

# Select column
column = st.selectbox("Select column to filter", df.columns)

# Select condition
if df[column].dtype in ['int64', 'float64']:
    condition = st.selectbox("Select condition", ["equals", "not equals", "greater than", "less than", "greater than or equal", "less than or equal"])
    value = st.number_input(f"Enter value for {column}")
elif df[column].dtype == 'object':
    condition = st.selectbox("Select condition", ["equals", "not equals", "contains", "does not contain"])
    value = st.text_input(f"Enter value for {column}")
else:
    st.write(f"Filtering not supported for column type: {df[column].dtype}")
    condition, value = None, None

# Apply the filter
if condition and value is not None:
    mask = apply_condition(column, condition, value)
    filtered_df = df[mask]

    # Display the filtered DataFrame
    st.subheader("Filtered DataFrame")
    st.write(filtered_df)


input_data = {
    "ID": [1, 2, 3, 4],
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Age": [24, 27, 22, 32]
}
output_data = {
    "UserID": [101, 102, 103, 104],
    "FullName": ["", "", "", ""],
    "Years": [0, 0, 0, 0]
}

input_df = pd.DataFrame(input_data)
output_df = pd.DataFrame(output_data)

st.title("tMap-like Widget for Field Mapping")

# Display the input DataFrame
st.subheader("Input DataFrame")
st.write(input_df)

# Display the output DataFrame
st.subheader("Output DataFrame")
st.write(output_df)

# Define the mapping logic
st.subheader("Field Mapping")

input_fields = list(input_df.columns)
output_fields = list(output_df.columns)

# Draggable list for input fields
st.write("Input Fields")
sorted_input_fields = sort_items(input_fields, key="input_fields", direction="vertical")

# Draggable list for output fields
st.write("Output Fields")
sorted_output_fields = sort_items(output_fields, key="output_fields", direction="vertical")

# Mapping fields
mapping = {}
for input_field, output_field in zip(sorted_input_fields, sorted_output_fields):
    mapping[input_field] = output_field
    st.write(f"{input_field} -> {output_field}")

# Example: Apply the mapping (transforming data based on mapping)
st.subheader("Transformed DataFrame")

transformed_df = pd.DataFrame()

for input_field, output_field in mapping.items():
    transformed_df[output_field] = input_df[input_field]

st.write(transformed_df)


