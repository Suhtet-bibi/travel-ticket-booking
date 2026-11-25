import sqlite3

def connect_db():
    conn = sqlite3.connect("travel_booking.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def setup_database():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS routes (
        route_id INTEGER PRIMARY KEY AUTOINCREMENT,
        destination TEXT NOT NULL,
        bus_name TEXT NOT NULL,
        price INTEGER NOT NULL,
        available_seats INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        passenger_name TEXT NOT NULL,
        route_id INTEGER,
        seat_no TEXT NOT NULL,
        FOREIGN KEY (route_id) REFERENCES routes (route_id)
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM routes")
    if cursor.fetchone()[0] == 0:
        sample_routes = [
            ("Yangon - Mandalay", "JJ Express", 30000, 10),
            ("Yangon - Bagan", "Mandalar Minn", 28000, 5),
            ("Yangon - Taunggyi", "Shwe Mandalar", 35000, 0),
        ]
        cursor.executemany(
            "INSERT INTO routes (destination, bus_name, price, available_seats) VALUES (?, ?, ?, ?)",
            sample_routes,
        )
        conn.commit()

    conn.close()

def get_all_routes():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM routes")
    routes = cursor.fetchall()
    conn.close()
    return routes

def get_route_by_id(route_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM routes WHERE route_id = ?", (route_id,))
    route = cursor.fetchone()
    conn.close()
    return route

def is_seat_taken(route_id, seat_no):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM bookings WHERE route_id = ? AND seat_no = ?",
        (route_id, seat_no),
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None


def save_booking(passenger_name, route_id, seat_no):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO bookings (passenger_name, route_id, seat_no) VALUES (?, ?, ?)",
        (passenger_name, route_id, seat_no),
    )

    cursor.execute(
        "UPDATE routes SET available_seats = available_seats - 1 WHERE route_id = ?",
        (route_id,),
    )

    conn.commit()
    conn.close()