import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",          # your username
    password="hari@6651",
    database="ai_project"
)

cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    product VARCHAR(50),
    sales INT,
    region VARCHAR(50)
)
""")

# Insert data
cursor.execute("""
INSERT INTO sales (product, sales, region)
VALUES
('Laptop', 1200, 'East'),
('Phone', 800, 'West'),
('Tablet', 300, 'North')
""")

conn.commit()

print("Table created and data inserted!")

cursor.close()
conn.close()
