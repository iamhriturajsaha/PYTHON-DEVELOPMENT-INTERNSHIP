import streamlit as st
import sqlite3
from datetime import datetime
# ---------------- Database Setup ----------------
conn = sqlite3.connect('trips.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS trips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                driver TEXT,
                distance REAL,
                time REAL,
                traffic TEXT,
                day TEXT,
                start_hour INTEGER,
                fare REAL,
                promo_code TEXT,
                created_at TEXT
            )''')
conn.commit()
# ---------------- Fare Calculator ----------------
class FareCalculator:
    BASE_FARE = 50
    PER_KM = 12
    PER_MIN = 2
    TRAFFIC_MULTIPLIERS = {
        "low": 1.0,
        "medium": 1.2,
        "high": 1.5
    }
    PEAK_HOURS = set(range(6, 10)) | set(range(18, 22))  # 6-9 AM & 6-9 PM
    PEAK_MULTIPLIER = 1.2
    WEEKEND_MULTIPLIER = 1.3

    PROMO_CODES = {
        "DISCOUNT10": 0.10,
        "SAVE20": 0.20,
        "FREERIDE": 1.0
    }
    @classmethod
    def calculate_fare(cls, distance, time, traffic, day, start_hour, promo_code=None):
        fare = cls.BASE_FARE + (distance * cls.PER_KM) + (time * cls.PER_MIN)
        fare *= cls.TRAFFIC_MULTIPLIERS.get(traffic, 1.0)
        if start_hour in cls.PEAK_HOURS:
            fare *= cls.PEAK_MULTIPLIER
        if day.lower() in ["saturday", "sunday"]:
            fare *= cls.WEEKEND_MULTIPLIER
        if promo_code and promo_code.upper() in cls.PROMO_CODES:
            discount = cls.PROMO_CODES[promo_code.upper()]
            fare *= (1 - discount)
        return round(fare, 2)
# ---------------- Database Functions ----------------
def add_trip(driver, distance, time, traffic, day, start_hour, fare, promo_code):
    query = '''INSERT INTO trips 
               (driver, distance, time, traffic, day, start_hour, fare, promo_code, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    conn.execute(query, (driver, distance, time, traffic, day, start_hour, fare, promo_code, datetime.now().isoformat()))
    conn.commit()
def get_all_trips():
    return conn.execute("SELECT * FROM trips").fetchall()
def get_driver_earnings():
    return conn.execute("SELECT driver, SUM(fare) as total_earnings FROM trips GROUP BY driver").fetchall()
# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Cab Fare Estimator", page_icon="🚖", layout="wide")
st.title("🚖 Cab Fare Estimator with Driver Reports")
menu = st.sidebar.radio("Navigation", ["Book Trip", "View Trips", "Driver Earnings Report"])
if menu == "Book Trip":
    st.header("📌 Book a New Trip")
    driver = st.text_input("Driver Name")
    distance = st.number_input("Distance (km)", min_value=1.0, step=0.5)
    time = st.number_input("Time (minutes)", min_value=1.0, step=1.0)
    traffic = st.selectbox("Traffic Condition", ["low", "medium", "high"])
    day = st.selectbox("Day of the Week", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
    start_hour = st.slider("Trip Start Hour", 0, 23, 9)
    promo_code = st.text_input("Promo Code (optional)").upper()
    if st.button("Estimate & Save Trip"):
        fare = FareCalculator.calculate_fare(distance, time, traffic, day, start_hour, promo_code)
        add_trip(driver, distance, time, traffic, day, start_hour, fare, promo_code)
        st.success(f"✅ Trip booked successfully! Estimated Fare: ₹{fare:.2f}")
elif menu == "View Trips":
    st.header("📜 All Trips")
    trips = get_all_trips()
    if trips:
        st.dataframe(trips)
    else:
        st.info("No trips found.")
elif menu == "Driver Earnings Report":
    st.header("💰 Driver-wise Earnings Report")
    report = get_driver_earnings()
    if report:
        st.table(report)
    else:
        st.info("No earnings data available.")
