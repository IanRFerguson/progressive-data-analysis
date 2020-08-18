# -------- IMPORTS

import os
import mysql.connector
import pandas as pd
import json

# -------- INSTANTIATE MARIA DB CONNECTION

with open("DB_Credentials.txt", "r") as incoming:                                       # Credentials stored in txt file
    credentials = json.load(incoming)

try:                                                                                    # Attempt to connect to MySQL instance with credentials
    connection = mysql.connector.connect(host=credentials["host"],
                                         database=credentials["database"],
                                         user=credentials["user"],
                                         password=credentials["password"])

    if connection.is_connected():                                                       # Print connection state, if successful
        db_Info = connection.get_server_info()
        print("Success! Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)


except Error as e:                                                                      # If error encountered, print message
    print("Error while connecting to MySQL", e)


all_tables = pd.read_sql("SHOW TABLES", connection)                                     # Store all tables in MySQL database in Pandas DataFrame
all_tables = list(all_tables["Tables_in_dsaanon"])                                      # Convert to list

try:
    os.mkdir("../00_CSV-DATA/")                                                         # Create new directory to output CSV files (unless it exists)
    print("New Directory Created")

except:
    print("Error: Cannot create directory")


# -------- HELPER FUNCTIONS

def scrapeMaria(keyword):

    """
    keyword <- Table name in DSA Anon database
    """

    output = pd.read_sql(("SELECT * FROM {}".format(keyword)), connection)              # Save all rows and columns from table to Pandas DataFrame
    return output


def pushToCSV(df, keyword):

    """
    df <- The DataFrame yieled from the scrapeMaria() function
    keyword <- Table name in DSA Anon database
    """

    path = ("../00_CSV-DATA/{}.csv".format(keyword))                                    # Format output file path
    df.to_csv(os.path.join(path), index=False)                                          # Push dataframe to CSV in local environment


# -------- KICK TO CSVs

for key in all_tables:                                                                  # Loop through tables and convert them to CSVs

    temp = scrapeMaria(key)
    pushToCSV(temp, key)
