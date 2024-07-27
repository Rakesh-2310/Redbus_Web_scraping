# **Redbus - Selenium web scrape and Streamlit Application**

## Overview

  This Streamlit application allows users to dynamically filter and visualize bus route data. The data is fetched from a MySQL database containing information scraped from the Redbus website. The application features various filters including route, bus type, price range, star rating, and minimum seats available. Users can interactively refine their search criteria and view the results in a tabular format.

## Features

•	**Dynamic Filtering**: Filter bus routes based on route name, bus type, price range, star rating, and available seats.

•	**Interactive Sliders**: Use sliders to specify price and rating ranges.

•	**Dropdown Menus**: Select routes and bus types from dropdown menus.

•	**Number Input**: Set minimum seats available using a numeric input field.

•	**Real-time Data Fetching**: Update the displayed data based on the selected filters.

## Prerequisites

•	Python 3.7 or higher

•	Streamlit

•	Pandas

•	PyMySQL

•	A MySQL database with the Redbus_webscraped_data schema

## Configuration

**Database Connection**: Update the host, user, passwd, and database parameters in the pymysql.connect function call to match your MySQL setup

**Run the Application:-**

•	From the terminal, navigate to the directory containing the script and run: streamlit run <script_name>.py

•	Replace <script_name> with the name of your Streamlit script file.

## **Dataset type and structure:-**

![image](https://github.com/user-attachments/assets/a1afaf5b-d6ee-410a-abf8-6655347fb68e)

**Flow Chart for web Scrapping and storing data:-**
Start **----->** Initialize WebDriver **----->** Navigate to Redbus Website **----->** Get Government state List **----->** Iterate through Government state **----->** Check for Pagination **----->** If Pagination Exists Iterate Through Pages **----->** Get each route link **----->** Iterate through Link and Extract Bus Data **----->** Store Data in Dictionary **----->** Convert Data to Data Frame **----->** Create MySQL Database and Table **----->** Insert Data into Database using automation **----->** End

**Flow Chart for data manipulation:-**
Start **----->** Connect to Database **----->** Read Table Data **----->** Check and Process Data **----->** Delete Rows **----->** Update Columns **----->** Convert Time **----->** Alter Schema **----->** Add and Update Columns **----->** End

**Flow Chart for Streamlit app:-**
Start **----->** Initialize Database Connection **----->** Display Filters Sidebar **----->** Fetch Filtered Data **----->** Display Data Table **----->** Close Database Connection after fetch **----->** End

Streamlit app:- 
![image](https://github.com/user-attachments/assets/b135d38c-a6bf-4718-a06c-f956efc80d37)


