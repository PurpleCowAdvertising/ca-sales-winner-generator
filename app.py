import streamlit as st
import pandas as pd
import random
import datetime

# Title and description for the app
st.title("CA Sales Winner Generator")
st.write("This tool generates random winners from a CA Sales campaign file.")


# Inputs for the campaign
campaign_name = st.text_input("Campaign Name", "example-campaign")
current_date = st.date_input("Draw Date")
number_of_winners = st.slider("Number of Winners", min_value=1, max_value=100, value=8)

# File upload widget for campaign file
uploaded_file = st.file_uploader("Upload Campaign File (Excel)", type=["xlsx"])

# Process the file if uploaded
if uploaded_file is not None:
    # Load the uploaded file as a pandas DataFrame
    df = pd.read_excel(uploaded_file)
    st.write("File successfully uploaded!")

    # Specify the column name to check for phone numbers
    column_name = 'CELL NO.'

    if column_name not in df.columns:
        st.error(f"Column '{column_name}' not found in the uploaded file. Please check the file format.")
    else:
        # Identify unique eligible cell numbers
        unique_cell_numbers = set(df[column_name].unique())

        # Check if there are enough eligible numbers to pick winners
        if len(unique_cell_numbers) < number_of_winners:
            st.error("Not enough unique eligible cell numbers to pick the specified number of winners.")
        else:
            # Randomly select winners
            winners = random.sample(unique_cell_numbers, number_of_winners)
            formatted_date = current_date.strftime('%d-%m-%Y')

            # Create a DataFrame for the winners
            winners_df = pd.DataFrame({
                'Date': [formatted_date] * number_of_winners,
                'Cell Number': winners,
                'Campaign Name': [campaign_name] * number_of_winners
            })

            # Display the winners in the app
            st.success("Successfully picked winners!")
            st.write(winners_df)

            # Option to download the winners as a CSV file
            csv = winners_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Winners as CSV",
                data=csv,
                file_name=f"{campaign_name}_winners_{formatted_date}.csv",
                mime='text/csv',
            )
else:
    st.info("Please upload an Excel file to proceed.")
