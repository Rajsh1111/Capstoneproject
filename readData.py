import pyodbc
import pandas as pd

# Define your connection string
productMasterQuery="SELECT * FROM product_master"
productInventoryQuery="SELECT * FROM product_inventory"
salesDataQuery="SELECT * from salesdata"


def createDataFrame(query):
    conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=virtucart.database.windows.net;'
    r'DATABASE=virtucart;'
    r'UID=virtucart_admin;'
    r'PWD=Virtu_Cart2024;'
    )

    try:
        # Attempt to connect to the database
        conn = pyodbc.connect(conn_str)
        df = pd.read_sql(query, conn) 
        #print(df) 
        print("Connection successful!")
        return df 
    except pyodbc.Error as ex:
        print("Connection failed. Please check your connection string.")
        print("Error:", ex)

       

#product_df=createDataFrame(productMasterQuery) 
#product_inventory_df=createDataFrame(productInventoryQuery) 
#transection_df=createDataFrame(salesDataQuery)        