# railway_reservation_system.py
"""
CLI-based Indian Railway Reservation System
Features:
- Sign up & Login with input validation
- Ticket booking with class-wise seat allocation
- Train search using predefined/train API data
- PNR generation and status checking
- Ticket cancellation
- User booking history and cancellation status
"""

import mysql.connector as s
import random as r
import time as t
import datetime as d
import re

# ---------------------- DATABASE CONNECTION ------------------------
mycon = s.connect(host="localhost", user='root', password="Sachin@1234", database="RAILWAY")
if mycon.is_connected():
    print("\nConnected to RAILWAY database")

# ---------------------- GLOBAL VARIABLES --------------------------
booked_seats = {'SL': 0, '3A': 0, '2A': 0, '1A': 0}
seat_limit = 90

# ---------------------- VALIDATION FUNCTIONS ----------------------
def validate_mobile(mob):
    return mob.isdigit() and len(mob) == 10

def validate_email(email):
    return re.fullmatch(r"[^@\s]+@gmail\.com", email)

# ---------------------- PNR GENERATOR -----------------------------
def gen_pnr(src_station):
    zone_map = {'DELHI': 2, 'MUMBAI': 8, 'KOLKATA': 6, 'CHENNAI': 4}
    first = zone_map.get(src_station.upper(), r.randint(2, 8))
    last = r.randint(10**6, 10**7 - 1)
    return int(f"{first}{last}")

# ---------------------- SIGNUP FUNCTION ---------------------------
def signup():
    name = input('Name: ')
    while True:
        mob = input('Mobile (10 digits): ')
        if validate_mobile(mob): break
        print("Invalid mobile number!")

    while True:
        email = input('Email (@gmail.com): ')
        if validate_email(email): break
        print("Invalid email format!")

    username = input('Username: ')
    password = input('Password: ')
    cursor = mycon.cursor()
    try:
        cursor.execute("INSERT INTO signin VALUES (%s, %s, %s, %s, %s)", (name, username, int(mob), email, password))
        mycon.commit()
        print("Sign up successful! Please log in.")
    except:
        print("User or mobile/email already exists.")

# ---------------------- LOGIN FUNCTION ----------------------------
def login():
    username = input('Username: ')
    password = input('Password: ')
    cursor = mycon.cursor()
    cursor.execute("SELECT * FROM signin WHERE USERNAME=%s AND PSWRD=%s", (username, password))
    if cursor.fetchone():
        print("\nLogin successful!")
        return username
    else:
        print("\nInvalid username or password!")
        return None

# ---------------------- BOOKING FUNCTION --------------------------
def book_ticket(user):
    global booked_seats
    to_dest = input("To (Destination): ")
    from_dest = input("From: ")
    train_no = input("Train No: ")
    travel_date = input("Date (YYYY-MM-DD): ")
    name = input("Passenger Name: ")
    age = input("Age: ")

    print("Choose Class: 1) SL 2) 3A 3) 2A 4) 1A")
    class_map = {'1': 'SL', '2': '3A', '3': '2A', '4': '1A'}
    ch = input("Enter choice: ")
    cls = class_map.get(ch)

    if not cls:
        print("Invalid class selection!")
        return

    if booked_seats[cls] >= seat_limit:
        print(f"All seats full in {cls} class!")
        return

    booked_seats[cls] += 1
    seat_no = booked_seats[cls]
    pnr = gen_pnr(from_dest)

    cursor = mycon.cursor()
    try:
        cursor.execute("""INSERT INTO TICKET_BOOKING
                        (TO_DEST, FROM_DEST, NAME, AGE, TRAIN_NO, USERNAME, DATE_OF, BOOKING_ID, CLASS, SEAT_NO, TICKET)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'CNF')""",
                       (to_dest, from_dest, name, age, train_no, user, travel_date, str(pnr), cls, seat_no))
        cursor.execute("INSERT INTO BOOKING_ID VALUES (%s, %s)", (str(pnr), d.datetime.now().date()))
        mycon.commit()
        print("\n--- TICKET BOOKED ---")
        print(f"PNR: {pnr}, Seat: {seat_no}, Class: {cls}, Status: CNF")
    except Exception as e:
        print("Booking failed:", e)

# ---------------------- PNR STATUS -------------------------------
def pnr_status():
    pnr = input("Enter PNR: ")
    cursor = mycon.cursor()
    cursor.execute("SELECT * FROM TICKET_BOOKING WHERE BOOKING_ID=%s", (pnr,))
    data = cursor.fetchone()
    if data:
        print("\n--- PNR STATUS ---")
        print("Passenger:", data[2])
        print("Train No:", data[4])
        print("From:", data[1], "To:", data[0])
        print("Class:", data[8], "Seat:", data[9])
        print("Status:", data[10])
    else:
        print("Invalid or Cancelled PNR")

# ---------------------- CANCELLATION -----------------------------
def cancel_ticket(user):
    name = input("Enter passenger name: ")
    date = input("Date of journey: ")
    cursor = mycon.cursor()
    cursor.execute("""SELECT * FROM TICKET_BOOKING
                      WHERE USERNAME=%s AND NAME=%s AND DATE_OF=%s AND TICKET!='CANCELLED'""",
                   (user, name, date))
    data = cursor.fetchall()
    if data:
        for d in data:
            print(f"PNR: {d[7]}, Class: {d[8]}, Seat: {d[9]}")
        pnr = input("Enter PNR to cancel: ")
        cursor.execute("UPDATE TICKET_BOOKING SET TICKET='CANCELLED' WHERE BOOKING_ID=%s", (pnr,))
        mycon.commit()
        print("Ticket cancelled successfully.")
    else:
        print("No matching bookings found.")

# ---------------------- MAIN PROGRAM -----------------------------
fir = True
user = None
while fir:
    print("""\nWELCOME TO INDIAN RAILWAY
1) LOGIN
2) SIGN IN""")
    initiate = input("Enter 1 for Login, 2 for Sign Up: ")
    if initiate == '1':
        user = login()
        if user:
            fir = False
    elif initiate == '2':
        signup()
    else:
        print("Invalid input")

while True:
    print("""\nOPTIONS:
1) Book Ticket
2) Cancel Ticket
3) Check PNR Status
4) Exit""")
    x = input("Enter your choice: ")
    if x == '1':
        book_ticket(user)
    elif x == '2':
        cancel_ticket(user)
    elif x == '3':
        pnr_status()
    elif x == '4':
        print("Goodbye!")
        break
    else:
        print("Invalid choice")
