import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page Configuration ---
# Set the title and a wide layout for the app page.
st.set_page_config(page_title="Nifty Stock Visualizer", layout="wide")


# --- Data Loading Function ---
# This function loads data from the CSV.
# The @st.cache_data decorator tells Streamlit to keep the data in a cache.
# This way, the data is loaded only once, making the app much faster.
@st.cache_data
def load_data(path):
    """
    Loads the stock data from a CSV file and converts the 'Date' column to datetime objects.
    """
    try:
        df = pd.read_csv(path)
        # It's important to convert the 'Date' column to a datetime format
        # for proper sorting and plotting on the x-axis.
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except FileNotFoundError:
        # Return None if the file is not found. The main app will handle this.
        return None

# --- Main Application ---

# Set a title for the web application.
st.title('📈 Nifty Stock Price Visualizer')

# Define the path to your CSV file.
# This assumes your script is in a folder, and the "Datasets" folder is one level up.
# Adjust the path if your folder structure is different.
file_path = "Nifty_Stocks.csv"

# Load the data using the function we defined.
df = load_data(file_path)

# --- App Logic ---
# Check if the dataframe was loaded successfully. If not, show an error.
if df is None:
    st.error(f"Error: The data file was not found.")
    st.info(f"Please ensure the file is located at the specified path: '{file_path}'")
else:
    # --- Sidebar for User Selections ---
    st.sidebar.header('📊 Select Your Stock')

    # 1. Category Selection Dropdown
    # Get the list of unique categories from the dataframe.
    category_list = df['Category'].unique()
    selected_category = st.sidebar.selectbox(
        'Select a Category:',
        options=category_list
    )

    # 2. Symbol Selection Dropdown
    # First, filter the dataframe based on the selected category.
    category_df = df[df['Category'] == selected_category]
    # Then, get the list of unique symbols for that category.
    symbol_list = category_df['Symbol'].unique()
    selected_symbol = st.sidebar.selectbox(
        'Select a Stock Symbol:',
        options=symbol_list
    )

    # --- Main Panel Display ---
    st.header(f"Displaying price history for: {selected_symbol}")
    st.markdown(f"**Category:** `{selected_category}`")

    # Filter the final dataframe for the selected symbol.
    symbol_df = df[df['Symbol'] == selected_symbol]

    # --- Display Stock Data Table ---
    st.subheader('Recent Stock Data')
    # Display the last 10 rows of the filtered data.
    st.dataframe(symbol_df.tail(10))

    # --- Display Stock Price Plot ---
    st.subheader('Closing Price History')

    # Create the plot figure.
    fig, ax = plt.subplots(figsize=(12, 6))

    # Use seaborn to draw the line plot.
    sns.lineplot(x='Date', y='Close', data=symbol_df, ax=ax, color='#007bff')

    # Customize the plot for better readability.
    ax.set_title(f'Closing Price for {selected_symbol}', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Closing Price (in INR)', fontsize=12)
    plt.xticks(rotation=45) # Rotate x-axis labels.
    plt.grid(True) # Add a grid.
    plt.tight_layout() # Adjust plot to ensure everything fits.

    # Display the plot in the Streamlit app.
    st.pyplot(fig)
