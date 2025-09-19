# 🚖 CAB FARE ESTIMATOR 

import sqlite3
from datetime import datetime
from statistics import mean
class Trip:
    """Represents a single cab ride."""
    def __init__(self, distance, time, traffic, day, start_hour, fare, driver, promo_code=None, timestamp=None):
        self.distance = distance      # in km
        self.time = time              # in minutes
        self.traffic = traffic.lower()
        self.day = day.capitalize()   # e.g., Monday
        self.start_hour = start_hour  # trip start time (0–23)
        self.fare = fare              # final fare
        self.driver = driver
        self.promo_code = promo_code
        self.timestamp = timestamp or datetime.now().isoformat()
    def __str__(self):
        return (
            f"Trip: Driver={self.driver}, Distance={self.distance} km, Time={self.time} min, "
            f"Traffic={self.traffic}, Day={self.day}, Hour={self.start_hour}, "
            f"Promo={self.promo_code}, Fare=₹{self.fare:.2f}, Time={self.timestamp}"
        )
class FareCalculator:
    """Handles dynamic fare calculation logic with surcharges and discounts."""
    # Base pricing
    BASE_FARE = 50
    PER_KM_RATE = 10
    PER_MIN_RATE = 2
    BOOKING_FEE = 20
    # Traffic multipliers
    TRAFFIC_MULTIPLIERS = {
        "light": 1.0,
        "medium": 1.10,
        "heavy": 1.25,
    }
    # Peak hours: 6–9 AM and 6–9 PM
    PEAK_HOURS = set(range(6, 10)) | set(range(18, 22))
    PEAK_MULTIPLIER = 1.20
    # Weekend multiplier
    WEEKEND_MULTIPLIER = 1.15
    # Promo codes
    PROMO_CODES = {
        "NEW50": {"type": "flat", "value": 50},       # flat ₹50 off
        "DISC10": {"type": "percent", "value": 10},   # 10% off
        "SAVE20": {"type": "percent", "value": 20},   # 20% off
    }
    @classmethod
    def calculate_fare(cls, distance, time, traffic, day, start_hour, promo_code=None):
        """Calculate total fare with surcharges and discounts."""
        # Base fare
        fare = cls.BASE_FARE + (distance * cls.PER_KM_RATE) + (time * cls.PER_MIN_RATE) + cls.BOOKING_FEE
        # Traffic multiplier
        fare *= cls.TRAFFIC_MULTIPLIERS.get(traffic.lower(), 1.0)
        # Peak hours
        if start_hour in cls.PEAK_HOURS:
            fare *= cls.PEAK_MULTIPLIER
        # Weekend
        if day.lower() in ["saturday", "sunday"]:
            fare *= cls.WEEKEND_MULTIPLIER
        # Promo code
        if promo_code and promo_code in cls.PROMO_CODES:
            discount = cls.PROMO_CODES[promo_code]
            if discount["type"] == "flat":
                fare -= discount["value"]
            elif discount["type"] == "percent":
                fare *= (1 - discount["value"] / 100)
        return max(round(fare, 2), 0.0)  # never negative
class CabSystem:
    """Manages trips, database persistence, and report generation."""
    def __init__(self, db_name="cab_system.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
    def create_table(self):
        """Create trips table if not exists."""
        query = """
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver TEXT,
            distance REAL,
            time INTEGER,
            traffic TEXT,
            day TEXT,
            start_hour INTEGER,
            fare REAL,
            promo_code TEXT,
            timestamp TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()
    def add_trip(self, distance, time, traffic, day, start_hour, driver, promo_code=None):
        """Add a trip to database and return the Trip object."""
        fare = FareCalculator.calculate_fare(distance, time, traffic, day, start_hour, promo_code)
        trip = Trip(distance, time, traffic, day, start_hour, fare, driver, promo_code)
        query = """
        INSERT INTO trips (driver, distance, time, traffic, day, start_hour, fare, promo_code, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.conn.execute(
            query,
            (driver, distance, time, traffic, day, start_hour, fare, promo_code, trip.timestamp),
        )
        self.conn.commit()
        return trip
    def fetch_trips(self):
        """Retrieve all trips as Trip objects."""
        query = "SELECT driver, distance, time, traffic, day, start_hour, fare, promo_code, timestamp FROM trips"
        rows = self.conn.execute(query).fetchall()
        return [
            Trip(
                distance=row[1],
                time=row[2],
                traffic=row[3],
                day=row[4],
                start_hour=row[5],
                fare=row[6],
                driver=row[0],
                promo_code=row[7],
                timestamp=row[8],
            )
            for row in rows
        ]
    def generate_report(self):
        """Generate overall system report."""
        trips = self.fetch_trips()
        if not trips:
            return "No trips recorded yet."
        total_earnings = sum(trip.fare for trip in trips)
        avg_fare = mean(trip.fare for trip in trips)
        traffic_summary = {t: sum(1 for trip in trips if trip.traffic == t) for t in ["light", "medium", "heavy"]}
        highest_trip = max(trips, key=lambda t: t.fare)
        lowest_trip = min(trips, key=lambda t: t.fare)
        report = [
            "----- Daily Report -----",
            f"Total Trips: {len(trips)}",
            f"Total Earnings: ₹{total_earnings:.2f}",
            f"Average Fare: ₹{avg_fare:.2f}",
            f"Traffic Summary: {traffic_summary}",
            f"Highest Fare Trip: ₹{highest_trip.fare:.2f} ({highest_trip.driver})",
            f"Lowest Fare Trip: ₹{lowest_trip.fare:.2f} ({lowest_trip.driver})",
        ]
        return "\n".join(report)
    def driver_report(self, driver_name):
        """Generate report for a specific driver."""
        query = "SELECT fare FROM trips WHERE driver=?"
        fares = [row[0] for row in self.conn.execute(query, (driver_name,)).fetchall()]
        if not fares:
            return f"No trips found for driver {driver_name}."
        report = [
            f"----- Driver Report: {driver_name} -----",
            f"Total Trips: {len(fares)}",
            f"Total Earnings: ₹{sum(fares):.2f}",
            f"Average Fare: ₹{mean(fares):.2f}",
        ]
        return "\n".join(report)
# User Input Mode
if __name__ == "__main__":
    cab_system = CabSystem()
    while True:
        print("\n🚖 Enter Trip Details (or type 'exit' to quit):")
        driver = input("Driver Name: ")
        if driver.lower() == "exit":
            break
        distance = float(input("Distance (km): "))
        time = int(input("Time (minutes): "))
        traffic = input("Traffic (light/medium/heavy): ")
        day = input("Day of the week: ")
        start_hour = int(input("Start Hour (0–23): "))
        promo_code = input("Promo Code (or press Enter to skip): ") or None
        trip = cab_system.add_trip(distance, time, traffic, day, start_hour, driver, promo_code)
        print("\n✅ Trip Recorded:", trip)
        # Show reports
        print("\n" + cab_system.generate_report())
        print("\n" + cab_system.driver_report(driver))


# Streamlit App Code
app_code = """
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
"""
# Save to app.py
with open("app.py", "w") as f:
    f.write(app_code)
print("✅ Streamlit app saved as app.py")


# Streamlit App Deployment
# Install necessary packages
!pip install -q streamlit pyngrok
# Import required libraries
import os
import time
from pyngrok import ngrok, conf
# Configure Ngrok Authentication
NGROK_AUTH_TOKEN = "2z0Oqv0tD166fELGCHwV2gLZwq1_2G2zUQRSs6C27k9vdzxwq"
conf.get_default().auth_token = NGROK_AUTH_TOKEN
# Create logs directory for Streamlit
LOG_DIR = "/content/logs"
os.makedirs(LOG_DIR, exist_ok=True)
# Kill any previous Streamlit or ngrok processes (to avoid port conflicts)
!pkill -f streamlit || echo "No existing streamlit process"
!pkill -f ngrok || echo "No existing ngrok process"
# Run Streamlit app in background on port 8501
!streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > {LOG_DIR}/app_log.txt 2>&1 &
# Give Streamlit a few seconds to start
time.sleep(7)
# Connect Ngrok to Streamlit
public_url = ngrok.connect(8501, "http")
print("🚖 Your Streamlit app is live at:", public_url.public_url)
# Show last 20 lines of log (helpful if error occurs)
!tail -n 20 {LOG_DIR}/app_log.txt
