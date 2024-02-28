import pyodbc

# Define your connection string
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
    print("Connection successful!")
except pyodbc.Error as ex:
    print("Connection failed. Please check your connection string.")
    print("Error:", ex)
