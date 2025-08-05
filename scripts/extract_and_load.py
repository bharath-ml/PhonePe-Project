import mysql.connector
import os
from dotenv import load_dotenv
import pandas as pd
import json

# Load environment variables from .env
load_dotenv()

# Get DB credentials
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Connect to MySQL
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)

cursor = conn.cursor()

# Create database if not exists
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
print(f"✅ Database '{db_name}' checked/created successfully.")

# Reconnect with the database specified
conn.database = db_name

# Step 1: Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS aggregated_transaction (
    State VARCHAR(255),
    Year VARCHAR(10),
    Quarter INT,
    Transacion_type VARCHAR(255),
    Transacion_count BIGINT,
    Transacion_amount DOUBLE
)
""")
print("✅ Table 'aggregated_transaction' checked/created successfully.")

# Step 2: Define path to data
data_path = r"D:\phonepe_data_dashboard\data\aggregated\transaction\country\india\state"

# Step 3: Load data into DataFrame
clm = {
    'State': [], 'Year': [], 'Quarter': [],
    'Transacion_type': [], 'Transacion_count': [], 'Transacion_amount': []
}

state_list = os.listdir(data_path)

for state in state_list:
    state_path = os.path.join(data_path, state)
    if not os.path.isdir(state_path):
        continue

    years = os.listdir(state_path)
    for year in years:
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        quarters = os.listdir(year_path)
        for quarter_file in quarters:
            try:
                file_path = os.path.join(year_path, quarter_file)
                with open(file_path, 'r') as file:
                    data = json.load(file)

                for txn in data['data']['transactionData']:
                    clm['State'].append(state)
                    clm['Year'].append(year)
                    clm['Quarter'].append(int(quarter_file.strip('.json')))
                    clm['Transacion_type'].append(txn['name'])
                    clm['Transacion_count'].append(txn['paymentInstruments'][0]['count'])
                    clm['Transacion_amount'].append(txn['paymentInstruments'][0]['amount'])
            except Exception as e:
                print(f"⚠️ Error reading/parsing file {file_path}: {e}")

# Step 4: Convert to DataFrame
df = pd.DataFrame(clm)
print("✅ DataFrame created with aggregated transaction data.")

# Step 5: Insert DataFrame into MySQL
insert_query = """
INSERT INTO aggregated_transaction 
(State, Year, Quarter, Transacion_type, Transacion_count, Transacion_amount)
VALUES (%s, %s, %s, %s, %s, %s)
"""

for row in df.itertuples(index=False):
    cursor.execute(insert_query, tuple(row))

conn.commit()
print("✅ Data inserted into MySQL table 'aggregated_transaction'.")

# Step 6: Cleanup
cursor.close()
conn.close()
print("✅ MySQL connection closed. All done!")






#*************************************************************aggregated_user***********************************
# Load environment variables
load_dotenv()

# Get DB credentials
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Connect to MySQL
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)

cursor = conn.cursor()

# Ensure the DB exists (optional safety)
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
print(f"✅ Database '{db_name}' checked/created successfully.")

# Use the database
conn.database = db_name  # ✅ Yes, this line is needed in each script




cursor.execute("""
CREATE TABLE IF NOT EXISTS aggregated_user (
    State VARCHAR(255),
    Year VARCHAR(10),
    Quarter INT,
    Device_Brand VARCHAR(255),
    User_Count BIGINT,
    User_Percentage FLOAT
)
""")
print("✅ Table 'aggregated_user' checked/created successfully.")

# Step 2: Define path to data
data_path = r"D:\phonepe_data_dashboard\data\aggregated\user\country\india\state"

# Step 3: Load data into DataFrame
clm = {
    'State': [], 'Year': [], 'Quarter': [],
    'Device_Brand': [], 'User_Count': [], 'User_Percentage': []
}

state_list = os.listdir(data_path)

for state in state_list:
    state_path = os.path.join(data_path, state)
    if not os.path.isdir(state_path):
        continue

    years = os.listdir(state_path)
    for year in years:
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        quarters = os.listdir(year_path)
        for quarter_file in quarters:
            try:
                file_path = os.path.join(year_path, quarter_file)
                with open(file_path, 'r') as file:
                    data = json.load(file)

                if data['data']['usersByDevice'] is not None:
                    for user in data['data']['usersByDevice']:
                        clm['State'].append(state)
                        clm['Year'].append(year)
                        clm['Quarter'].append(int(quarter_file.strip('.json')))
                        clm['Device_Brand'].append(user['brand'])
                        clm['User_Count'].append(user['count'])
                        clm['User_Percentage'].append(user['percentage'])

            except Exception as e:
                print(f"⚠️ Error reading/parsing file {file_path}: {e}")

# Step 4: Convert to DataFrame
df = pd.DataFrame(clm)
print("✅ DataFrame created with aggregated user data.")

# Step 5: Insert DataFrame into MySQL
insert_query = """
INSERT INTO aggregated_user 
(State, Year, Quarter, Device_Brand, User_Count, User_Percentage)
VALUES (%s, %s, %s, %s, %s, %s)
"""

for row in df.itertuples(index=False):
    cursor.execute(insert_query, tuple(row))

conn.commit()
print("✅ Data inserted into MySQL table 'aggregated_user'.")

# Step 6: Cleanup
cursor.close()
conn.close()
print("✅ MySQL connection closed. All done!")






#*******************************************************MAP_transaction***********************************************


# Load environment variables
load_dotenv()
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Connect to MySQL
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)
cursor = conn.cursor()

# Ensure DB exists and reconnect with it
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
conn.database = db_name
print(f"✅ Connected to database '{db_name}'")

# Step 1: Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS map_transaction (
    State VARCHAR(255),
    Year VARCHAR(10),
    Quarter INT,
    District VARCHAR(255),
    Transaction_count BIGINT,
    Transaction_amount DOUBLE
)
""")
print("✅ Table 'map_transaction' checked/created successfully.")

# Step 2: Define data path
data_path = r"D:\phonepe_data_dashboard\data\map\transaction\hover\country\india\state"

clm = {
    'State': [], 'Year': [], 'Quarter': [],
    'District': [], 'Transaction_count': [], 'Transaction_amount': []
}

state_list = os.listdir(data_path)

# Step 3: Extract data
for state in state_list:
    state_path = os.path.join(data_path, state)
    if not os.path.isdir(state_path):
        continue

    years = os.listdir(state_path)
    for year in years:
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        quarters = os.listdir(year_path)
        for quarter_file in quarters:
            try:
                file_path = os.path.join(year_path, quarter_file)
                with open(file_path, 'r') as file:
                    data = json.load(file)

                for district_info in data['data']['hoverDataList']:
                    clm['State'].append(state)
                    clm['Year'].append(year)
                    clm['Quarter'].append(int(quarter_file.strip('.json')))
                    clm['District'].append(district_info['name'])
                    clm['Transaction_count'].append(district_info['metric'][0]['count'])
                    clm['Transaction_amount'].append(district_info['metric'][0]['amount'])

            except Exception as e:
                print(f"⚠️ Error parsing {file_path}: {e}")

# Step 4: Create DataFrame
df = pd.DataFrame(clm)
print("✅ DataFrame created for 'map_transaction'.")

# Step 5: Insert into MySQL
insert_query = """
INSERT INTO map_transaction 
(State, Year, Quarter, District, Transaction_count, Transaction_amount)
VALUES (%s, %s, %s, %s, %s, %s)
"""

for row in df.itertuples(index=False):
    cursor.execute(insert_query, tuple(row))

conn.commit()
print("✅ Data inserted into 'map_transaction'.")

# Cleanup
cursor.close()
conn.close()
print("✅ MySQL connection closed.")

#************************************************************************MAP_USER*************************
# Load environment variables
load_dotenv()
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Connect to MySQL
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)
cursor = conn.cursor()

# Ensure DB exists and reconnect
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
conn.database = db_name
print(f"✅ Connected to database '{db_name}'")

# Step 1: Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS map_user (
    State VARCHAR(255),
    Year VARCHAR(10),
    Quarter INT,
    District VARCHAR(255),
    RegisteredUsers BIGINT,
    AppOpens BIGINT
)
""")
print("✅ Table 'map_user' checked/created successfully.")

# Step 2: Set path
data_path = r"D:\phonepe_data_dashboard\data\map\user\hover\country\india\state"

clm = {
    'State': [], 'Year': [], 'Quarter': [],
    'District': [], 'RegisteredUsers': [], 'AppOpens': []
}

# Step 3: Extract data
for state in os.listdir(data_path):
    state_path = os.path.join(data_path, state)
    if not os.path.isdir(state_path):
        continue

    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        for quarter_file in os.listdir(year_path):
            file_path = os.path.join(year_path, quarter_file)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)

                hover_data = data['data']['hoverData']
                for district, values in hover_data.items():
                    clm['State'].append(state)
                    clm['Year'].append(year)
                    clm['Quarter'].append(int(quarter_file.strip('.json')))
                    clm['District'].append(district)
                    clm['RegisteredUsers'].append(values.get('registeredUsers', 0))
                    clm['AppOpens'].append(values.get('appOpens', 0))

            except Exception as e:
                print(f"⚠️ Error parsing {file_path}: {e}")

# Step 4: Create DataFrame
df = pd.DataFrame(clm)
print("✅ DataFrame created for 'map_user'.")

# Step 5: Insert into MySQL
insert_query = """
INSERT INTO map_user 
(State, Year, Quarter, District, RegisteredUsers, AppOpens)
VALUES (%s, %s, %s, %s, %s, %s)
"""

for row in df.itertuples(index=False):
    cursor.execute(insert_query, tuple(row))

conn.commit()
print("✅ Data inserted into 'map_user'.")

# Cleanup
cursor.close()
conn.close()
print("✅ MySQL connection closed.")

#***********************************************************************TOP_TRANSACTION*******************************************
# Load environment variables
load_dotenv()
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Connect to MySQL
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)
cursor = conn.cursor()

# Ensure DB exists and reconnect
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
conn.database = db_name
print(f"✅ Connected to database '{db_name}'")

# Step 1: Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS top_transaction (
    State VARCHAR(255),
    Year VARCHAR(10),
    Quarter INT,
    District VARCHAR(255),
    Transaction_count BIGINT,
    Transaction_amount DOUBLE
)
""")
print("✅ Table 'top_transaction' checked/created successfully.")

# Step 2: Set path
data_path = r"D:\phonepe_data_dashboard\data\top\transaction\country\india\state"

clm = {
    'State': [], 'Year': [], 'Quarter': [],
    'District': [], 'Transaction_count': [], 'Transaction_amount': []
}

# Step 3: Extract data
for state in os.listdir(data_path):
    state_path = os.path.join(data_path, state)
    if not os.path.isdir(state_path):
        continue

    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        for quarter_file in os.listdir(year_path):
            file_path = os.path.join(year_path, quarter_file)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)

                districts = data['data'].get('districts', [])
                for district in districts:
                    clm['State'].append(state)
                    clm['Year'].append(year)
                    clm['Quarter'].append(int(quarter_file.strip('.json')))
                    clm['District'].append(district.get('entityName', 'Unknown'))
                    clm['Transaction_count'].append(district['metric'].get('count', 0))
                    clm['Transaction_amount'].append(district['metric'].get('amount', 0.0))

            except Exception as e:
                print(f"⚠️ Error parsing {file_path}: {e}")

# Step 4: Create DataFrame
df = pd.DataFrame(clm)
print("✅ DataFrame created for 'top_transaction'.")

# Step 5: Insert into MySQL
insert_query = """
INSERT INTO top_transaction 
(State, Year, Quarter, District, Transaction_count, Transaction_amount)
VALUES (%s, %s, %s, %s, %s, %s)
"""

for row in df.itertuples(index=False):
    cursor.execute(insert_query, tuple(row))

conn.commit()
print("✅ Data inserted into 'top_transaction'.")

# Cleanup
cursor.close()
conn.close()
print("✅ MySQL connection closed.")

#***************************************************************TOP_USER****************************************
# Load environment variables
load_dotenv()
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Connect to MySQL
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)
cursor = conn.cursor()

# Ensure database exists and reconnect
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
conn.database = db_name
print(f"✅ Connected to database '{db_name}'")

# Step 1: Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS top_user (
    State VARCHAR(255),
    Year VARCHAR(10),
    Quarter INT,
    District VARCHAR(255),
    Registered_users BIGINT,
    App_opens BIGINT
)
""")
print("✅ Table 'top_user' checked/created successfully.")

# Step 2: Set path
data_path = r"D:\phonepe_data_dashboard\data\top\user\country\india\state"

clm = {
    'State': [], 'Year': [], 'Quarter': [],
    'District': [], 'Registered_users': [], 'App_opens': []
}

# Step 3: Extract data
for state in os.listdir(data_path):
    state_path = os.path.join(data_path, state)
    if not os.path.isdir(state_path):
        continue

    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        for quarter_file in os.listdir(year_path):
            file_path = os.path.join(year_path, quarter_file)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)

                districts = data['data'].get('districts', [])
                for district in districts:
                    clm['State'].append(state)
                    clm['Year'].append(year)
                    clm['Quarter'].append(int(quarter_file.strip('.json')))
                    clm['District'].append(district.get('name', 'Unknown'))
                    clm['Registered_users'].append(district.get('registeredUsers', 0))
                    clm['App_opens'].append(district.get('appOpens', 0))

            except Exception as e:
                print(f"⚠️ Error parsing {file_path}: {e}")

# Step 4: Create DataFrame
df = pd.DataFrame(clm)
print("✅ DataFrame created for 'top_user'.")

# Step 5: Insert into MySQL
insert_query = """
INSERT INTO top_user 
(State, Year, Quarter, District, Registered_users, App_opens)
VALUES (%s, %s, %s, %s, %s, %s)
"""

for row in df.itertuples(index=False):
    cursor.execute(insert_query, tuple(row))

conn.commit()
print("✅ Data inserted into 'top_user'.")

# Cleanup
cursor.close()
conn.close()
print("✅ MySQL connection closed.")

#************************************************************AGGREGATED_INSURANCE**********************************************

# Load credentials
load_dotenv()
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Connect
conn = mysql.connector.connect(host=host, user=user, password=password)
cursor = conn.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
conn.database = db_name
print("✅ Connected to database.")

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS aggregated_insurance (
    State VARCHAR(255),
    Year VARCHAR(10),
    Quarter INT,
    Insurance_type VARCHAR(255),
    Insurance_count BIGINT,
    Insurance_amount DOUBLE
)
""")
print("✅ Table 'aggregated_insurance' created.")

# Load data
path = r"D:\phonepe_data_dashboard\data\aggregated\insurance\country\india\state"
clm = {'State': [], 'Year': [], 'Quarter': [], 'Insurance_type': [], 'Insurance_count': [], 'Insurance_amount': []}

for state in os.listdir(path):
    for year in os.listdir(os.path.join(path, state)):
        for file in os.listdir(os.path.join(path, state, year)):
            try:
                with open(os.path.join(path, state, year, file), 'r') as f:
                    data = json.load(f)

                for entry in data['data']['transactionData']:
                    clm['State'].append(state)
                    clm['Year'].append(year)
                    clm['Quarter'].append(int(file.strip('.json')))
                    clm['Insurance_type'].append(entry['name'])
                    clm['Insurance_count'].append(entry['paymentInstruments'][0]['count'])
                    clm['Insurance_amount'].append(entry['paymentInstruments'][0]['amount'])
            except Exception as e:
                print(f"⚠️ Error reading {file}: {e}")

df = pd.DataFrame(clm)
print("✅ DataFrame created for 'aggregated_insurance'.")

# Insert into SQL
insert_query = """
INSERT INTO aggregated_insurance 
(State, Year, Quarter, Insurance_type, Insurance_count, Insurance_amount)
VALUES (%s, %s, %s, %s, %s, %s)
"""
for row in df.itertuples(index=False):
    cursor.execute(insert_query, tuple(row))

conn.commit()
print("✅ Data inserted into 'aggregated_insurance'.")
cursor.close()
conn.close()


#*************************************************MAP_INSURANCE*********************************
import os
import json
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Connect to MySQL
conn = mysql.connector.connect(host=host, user=user, password=password)
cursor = conn.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
conn.database = db_name

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS map_insurance (
    State VARCHAR(255),
    Year VARCHAR(10),
    Quarter INT,
    District VARCHAR(255),
    Latitude DOUBLE,
    Longitude DOUBLE,
    Insurance_Count BIGINT
)
""")

# Path to data
data_path = r"D:\phonepe_data_dashboard\data\map\insurance\country\india\state"

clm = {
    'State': [], 'Year': [], 'Quarter': [],
    'District': [], 'Latitude': [], 'Longitude': [],
    'Insurance_Count': []
}

state_list = os.listdir(data_path)

for state in state_list:
    state_path = os.path.join(data_path, state)
    if not os.path.isdir(state_path):
        continue

    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        for quarter_file in os.listdir(year_path):
            file_path = os.path.join(year_path, quarter_file)
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                columns_in_file = data.get("data", {}).get("columns", [])
                entries = data.get("data", {}).get("data", [])
                for row in entries:
                    row_dict = dict(zip(columns_in_file, row))
                    lat = row_dict.get("lat")
                    lng = row_dict.get("lng")
                    metric = row_dict.get("metric")
                    district = row_dict.get("label")
                    if None in [lat, lng, metric, district]:
                        continue
                    clm["State"].append(state)
                    clm["Year"].append(year)
                    clm["Quarter"].append(int(quarter_file.strip(".json")))
                    clm["District"].append(district)
                    clm["Latitude"].append(lat)
                    clm["Longitude"].append(lng)
                    clm["Insurance_Count"].append(int(metric))
            except Exception as e:
                print(f"⚠️ Error processing {file_path}: {e}")

# Convert to DataFrame
df = pd.DataFrame(clm)
print(f"✅ DataFrame created with {len(df)} records.")

# Insert DataFrame into MySQL
insert_query = """
INSERT INTO map_insurance 
(State, Year, Quarter, District, Latitude, Longitude, Insurance_Count)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

for row in df.itertuples(index=False):
    cursor.execute(insert_query, tuple(row))

conn.commit()
print("✅ Data inserted into MySQL table 'map_insurance'.")

cursor.close()
conn.close()
print("✅ MySQL connection closed. All done!")


#*************************************TOP_INSURANCE*****************************
load_dotenv()

# DB Credentials
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Connect to MySQL
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)
cursor = conn.cursor()

# Create DB if not exists
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
conn.database = db_name

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS top_insurance (
    State VARCHAR(255),
    Year VARCHAR(10),
    Quarter INT,
    Pincode VARCHAR(20),
    Count BIGINT,
    Amount DOUBLE
)
""")
print("✅ Table 'top_insurance' checked/created successfully.")

# Define path
data_path = r"D:\phonepe_data_dashboard\data\top\insurance\country\india\state"

# Collect data
clm = {
    'State': [], 'Year': [], 'Quarter': [],
    'Pincode': [], 'Count': [], 'Amount': []
}

states = os.listdir(data_path)

for state in states:
    state_path = os.path.join(data_path, state)
    if not os.path.isdir(state_path):
        continue

    years = os.listdir(state_path)
    for year in years:
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path):
            continue

        quarters = os.listdir(year_path)
        for quarter_file in quarters:
            file_path = os.path.join(year_path, quarter_file)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)

                pincodes = data['data'].get('pincodes', [])
                for entry in pincodes:
                    clm['State'].append(state)
                    clm['Year'].append(year)
                    clm['Quarter'].append(int(quarter_file.strip('.json')))
                    clm['Pincode'].append(entry['entityName'])
                    clm['Count'].append(entry['metric']['count'])
                    clm['Amount'].append(entry['metric']['amount'])
            except Exception as e:
                print(f"⚠️ Error parsing {file_path}: {e}")

# Create DataFrame
df = pd.DataFrame(clm)
print(f"✅ DataFrame created with {len(df)} records.")

# Insert into MySQL
insert_query = """
INSERT INTO top_insurance 
(State, Year, Quarter, Pincode, Count, Amount)
VALUES (%s, %s, %s, %s, %s, %s)
"""

for row in df.itertuples(index=False):
    cursor.execute(insert_query, tuple(row))

conn.commit()
print("✅ Data inserted into MySQL table 'top_insurance'.")

# Cleanup
cursor.close()
conn.close()
print("✅ MySQL connection closed. All done!")