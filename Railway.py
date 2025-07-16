import mysql.connector as s

# Connect to MySQL (root user, no database initially)
mycon = s.connect(
    host="localhost",
    user="root",
    password="Sachin@1234"
)

cursor = mycon.cursor()

# Step 1: Create Database
cursor.execute("CREATE DATABASE IF NOT EXISTS RAILWAY")
cursor.execute("USE RAILWAY")

# Step 2: Create signin table
cursor.execute("""
CREATE TABLE IF NOT EXISTS signin (
    name VARCHAR(100),
    username VARCHAR(50) PRIMARY KEY,
    mobile BIGINT UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    pswrd VARCHAR(50) NOT NULL
)
""")

# Step 3: Create TICKET_BOOKING table
cursor.execute("""
CREATE TABLE IF NOT EXISTS TICKET_BOOKING (
    to_destination VARCHAR(100),
    from_destination VARCHAR(100),
    name VARCHAR(100),
    age INT,
    train_no INT,
    username VARCHAR(50),
    date_of DATE,
    booking_id VARCHAR(20) PRIMARY KEY,
    class VARCHAR(5),
    seat_no INT,
    ticket VARCHAR(20) DEFAULT 'CNF',
    FOREIGN KEY (username) REFERENCES signin(username)
)
""")

# Step 4: Create BOOKING_ID table
cursor.execute("""
CREATE TABLE IF NOT EXISTS BOOKING_ID (
    booking_id VARCHAR(20),
    booking_date DATE
)
""")

# Step 5 (Optional): Create TRAIN_LIST table
cursor.execute("""
CREATE TABLE IF NOT EXISTS TRAIN_LIST (
    train_no INT PRIMARY KEY,
    train_name VARCHAR(100),
    from_station VARCHAR(100),
    to_station VARCHAR(100),
    departure_time TIME,
    arrival_time TIME,
    runs_on VARCHAR(20)
)
""")

print("✅ All tables created successfully in RAILWAY database.")

mycon.close()
