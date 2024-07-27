import streamlit as st
import pandas as pd
import pymysql
from datetime import time

# Establish a connection to the database
connection = pymysql.connect(
    host='127.0.0.1', 
    user='root', 
    passwd='Krisrak@123', 
    database='Redbus_webscraped_data'
)

# Function to get distinct column values from the database with filters
def get_values(column_name, route=None, bustype=None):
    query = f"SELECT DISTINCT {column_name} AS value FROM Redbus_webscraped_data.bus_routes WHERE 1=1"
    if bustype:
        query += f" AND bustype = '{bustype}'"
    if route:
        query += f" AND route_name = '{route}'"
    column_values = pd.read_sql(query, connection)
    return column_values['value'].tolist()

# Function to get data from the database
def get_data(route=None, bustype=None, min_price=None, min_rating=None, max_rating=None, min_seats=None, dep_time=None, arr_time=None):
    query = """
    SELECT 
    route_Departure_name as Departure,
    route_Arrival_name as Arrival,
    busname as Busname,
    bustype as Bustype,
    departing_time as `Departing Time`,
    reaching_time as `Reaching Time`,
    duration as Duration,
    star_rating as Rating,
    price as Price,
    seats_available as `Seats Available`
    FROM Redbus_webscraped_data.bus_routes WHERE 1=1
    """
    if bustype:
        query += f" AND bustype = '{bustype}'"
    if route:
        query += f" AND route_name = '{route}'"
    if min_price is not None:
        query += f" AND price >= {min_price}"
    if min_rating is not None:
        query += f" AND star_rating >= {min_rating}"
    if max_rating is not None:
        query += f" AND star_rating <= {max_rating}"
    if min_seats is not None:
        query += f" AND seats_available >= {min_seats}"
    if dep_time is not None:
        query += f" AND TIME(departing_time) >= '{dep_time}'"
    if arr_time is not None:
        query += f" AND TIME(reaching_time) <= '{arr_time}'"

    df = pd.read_sql(query, connection)
    return df

# Streamlit UI
st.title("Bus Route Filter")

# Sidebar for filters
with st.sidebar:
    st.header("Filters")

    # Fetch initial unique values for route
    route_name_values = get_values('route_name')

    # Dropdown for route
    if 'route' not in st.session_state:
        st.session_state['route'] = 'All'
    route = st.selectbox("Route", options=['All'] + route_name_values, key='route')
    route = None if route == "All" else route

    # Update bustype dropdown based on selected route
    bustype_values = get_values('bustype', route=route)
    if 'bustype' not in st.session_state:
        st.session_state['bustype'] = 'All'
    bustype = st.selectbox("Bus Type", options=['All'] + bustype_values, key='bustype')
    bustype = None if bustype == "All" else bustype

    # Number input for minimum seats available
    if 'min_seats' not in st.session_state:
        st.session_state['min_seats'] = 0
    min_seats = st.number_input("Min Seats Available", min_value=0, value=st.session_state['min_seats'], key='min_seats')

    # Input for minimum price
    if 'min_price' not in st.session_state:
        st.session_state['min_price'] = 0
    min_price = st.number_input("Min Price", min_value=0, value=st.session_state['min_price'], key='min_price')

    # Slider for star rating
    if 'star_rating' not in st.session_state:
        st.session_state['star_rating'] = (0.0, 5.0)
    star_rating = st.slider("Rating", min_value=0.0, max_value=5.0, value=st.session_state['star_rating'], step=0.1, key='star_rating')
    min_rating, max_rating = star_rating

    # Time input for departing time
    if 'dep_time' not in st.session_state:
        st.session_state['dep_time'] = time(0, 0)
    dep_time = st.time_input("Departing Time After", value=st.session_state['dep_time'], key='dep_time')

    # Time input for reaching time
    if 'arr_time' not in st.session_state:
        st.session_state['arr_time'] = time(23, 59)
    arr_time = st.time_input("Reaching Time Before", value=st.session_state['arr_time'], key='arr_time')

    # Reset button
    if st.button("Reset Filters"):
        route = None
        bustype = None
        min_seats = 0
        min_price = 0
        min_rating = 0.0
        max_rating = 5.0
        dep_time = time(0, 0)
        arr_time = time(23, 59)

# Main area for displaying data
data = get_data(
    route, 
    bustype, 
    min_price, 
    min_rating, 
    max_rating, 
    min_seats, 
    dep_time, 
    arr_time
)
st.dataframe(data)

# Closing the database connection after the application has finished fetching data
connection.close()
