import mysql.connector


with open('database/create_table.sql', 'r') as f:
    query = f.read()



# Connect to MySQL
conn = mysql.connector.connect(
  host="localhost",
  user=MYSQL_USER,
  password=MYSQL_PASSWORD,
  database="chatbot"
)
