import streamlit as st
import pandas as pd
import pymysql

# Establish a connection to the database
connection = pymysql.connect(host='127.0.0.1', user='root', passwd='Krisrak@123', database='Redbus_webscraped_data')

# Function to get distinct column values from the database with filters
def get_values(column_name, route=None, bustype=None, min_price=None, max_price=None, min_rating=None, max_rating=None, min_seats=None):
    query = f"SELECT DISTINCT {column_name} AS value FROM Redbus_webscraped_data.bus_routes WHERE 1=1"
    if bustype:
        query += f" AND bustype = '{bustype}'"
    if route:
        query += f" AND route_name = '{route}'"
    if min_price is not None:
        query += f" AND price >= {min_price}"
    if max_price is not None:
        query += f" AND price <= {max_price}"
    if min_rating is not None:
        query += f" AND star_rating >= {min_rating}"
    if max_rating is not None:
        query += f" AND star_rating <= {max_rating}"
    if min_seats is not None:
        query += f" AND seats_available >= {min_seats}"
    column_values = pd.read_sql(query, connection)
    return column_values['value'].tolist()

def get_min_value(column_name, route=None, bustype=None):
    query = f"SELECT MIN({column_name}) AS value FROM Redbus_webscraped_data.bus_routes WHERE 1=1"
    if route:
        query += f" AND route_name = '{route}'"
    if bustype:
        query += f" AND bustype = '{bustype}'"
    column_values = pd.read_sql(query, connection)
    return column_values['value'][0] if not column_values.empty else None

def get_max_value(column_name, route=None, bustype=None):
    query = f"SELECT MAX({column_name}) AS value FROM Redbus_webscraped_data.bus_routes WHERE 1=1"
    if route:
        query += f" AND route_name = '{route}'"
    if bustype:
        query += f" AND bustype = '{bustype}'"
    column_values = pd.read_sql(query, connection)
    return column_values['value'][0] if not column_values.empty else None

# Function to get data from the database
def get_data(route=None, bustype=None, min_price=None, max_price=None, min_rating=None, max_rating=None, min_seats=None):
    query = """
    SELECT 
    route_Departure_name as Departure,
    route_Arrival_name as Arrival,
    busname as Busname,
    bustype as Bustype,
    route_link as `Route Link`,
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
    if max_price is not None:
        query += f" AND price <= {max_price}"
    if min_rating is not None:
        query += f" AND star_rating >= {min_rating}"
    if max_rating is not None:
        query += f" AND star_rating <= {max_rating}"
    if min_seats is not None:
        query += f" AND seats_available >= {min_seats}"
    
    df = pd.read_sql(query, connection)
    return df

# Streamlit UI
st.title("Bus Route Filter")

# Fetch initial unique values for route
route_name_values = get_values('route_name')

# Dropdown for route
route = st.selectbox("Route", options=['All'] + route_name_values)
route = None if route == "All" else route

# Update bustype dropdown based on selected route
bustype_values = get_values('bustype', route=route)
bustype = st.selectbox("Bus Type", options=['All'] + bustype_values)
bustype = None if bustype == "All" else bustype

# Number input for minimum seats available
min_seats = st.number_input("Min Seats Available", min_value=0, value=0)

# Update min and max values for price and rating based on current filters
price_min = get_min_value('price', route=route, bustype=bustype)
price_max = get_max_value('price', route=route, bustype=bustype)
rating_min = get_min_value('star_rating', route=route, bustype=bustype)
rating_max = get_max_value('star_rating', route=route, bustype=bustype)

# Handle cases where min_value is equal to max_value for sliders
price_min = price_min if price_min is not None else 0
price_max = price_max if price_max is not None else 1
if price_min == price_max:
    price_max += 1

rating_min = rating_min if rating_min is not None else 0
rating_max = rating_max if rating_max is not None else 1
if rating_min == rating_max:
    rating_max += 0.1

# Sliders for price and rating
price = st.slider("Price Range", min_value=float(price_min), max_value=float(price_max), value=(float(price_min), float(price_max)), step=1.0)
star_rating = st.slider("Rating Range", min_value=float(rating_min), max_value=float(rating_max), value=(float(rating_min), float(rating_max)), step=0.1)

min_price, max_price = price
min_rating, max_rating = star_rating

# Button to fetch data
if st.button("Fetch Data"):
    data = get_data(route, bustype, min_price, max_price, min_rating, max_rating, min_seats)
    st.dataframe(data)

# Closing the database connection after the application has finished fetching data
connection.close()
