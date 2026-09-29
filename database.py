import sqlite3
from datetime import datetime, timedelta

DB_NAME = "appointments.db"


def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            experience INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            available INTEGER DEFAULT 1,
            FOREIGN KEY (doctor_id) REFERENCES doctors(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            doctor_id INTEGER NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (doctor_id) REFERENCES doctors(id)
        )
    """)

    doctor_count = cursor.execute(
        "SELECT COUNT(*) FROM doctors"
    ).fetchone()[0]

    if doctor_count == 0:
        doctors = [
            ("Dr. Anil Kumar", "Cardiology", 12),
            ("Dr. Priya Sharma", "Dermatology", 8),
            ("Dr. Ravi Teja", "Dentistry", 10),
            ("Dr. Sneha Rao", "Orthopedics", 9),
            ("Dr. Arjun Mehta", "Neurology", 11),
            ("Dr. Kavya Singh", "General Medicine", 7)
        ]

        cursor.executemany(
            """
            INSERT INTO doctors
            (name, department, experience)
            VALUES (?, ?, ?)
            """,
            doctors
        )

    doctors = cursor.execute(
        "SELECT id FROM doctors"
    ).fetchall()

    times = [
        "09:00 AM",
        "10:30 AM",
        "12:00 PM",
        "02:00 PM",
        "03:30 PM",
        "05:00 PM"
    ]

    for doctor in doctors:
        for day in range(30):

            date_value = (
                datetime.now() + timedelta(days=day)
            ).strftime("%Y-%m-%d")

            for time in times:

                existing = cursor.execute(
                    """
                    SELECT id FROM slots
                    WHERE doctor_id = ?
                    AND appointment_date = ?
                    AND appointment_time = ?
                    """,
                    (
                        doctor["id"],
                        date_value,
                        time
                    )
                ).fetchone()

                if not existing:
                    cursor.execute(
                        """
                        INSERT INTO slots
                        (
                            doctor_id,
                            appointment_date,
                            appointment_time,
                            available
                        )
                        VALUES (?, ?, ?, 1)
                        """,
                        (
                            doctor["id"],
                            date_value,
                            time
                        )
                    )

    connection.commit()
    connection.close()


def get_doctors():

    connection = get_connection()

    doctors = connection.execute(
        """
        SELECT *
        FROM doctors
        ORDER BY department, name
        """
    ).fetchall()

    connection.close()

    return [dict(doctor) for doctor in doctors]


def get_available_slots(doctor_id, date):

    connection = get_connection()

    slots = connection.execute(
        """
        SELECT *
        FROM slots
        WHERE doctor_id = ?
        AND appointment_date = ?
        AND available = 1
        ORDER BY appointment_time
        """,
        (doctor_id, date)
    ).fetchall()

    connection.close()

    return [dict(slot) for slot in slots]


def book_appointment(
    patient_name,
    phone,
    doctor_id,
    appointment_date,
    appointment_time
):

    connection = get_connection()

    slot = connection.execute(
        """
        SELECT *
        FROM slots
        WHERE doctor_id = ?
        AND appointment_date = ?
        AND appointment_time = ?
        AND available = 1
        """,
        (
            doctor_id,
            appointment_date,
            appointment_time
        )
    ).fetchone()

    if not slot:
        connection.close()

        return {
            "success": False,
            "message": "This appointment slot is no longer available."
        }

    connection.execute(
        """
        INSERT INTO appointments
        (
            patient_name,
            phone,
            doctor_id,
            appointment_date,
            appointment_time,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            patient_name,
            phone,
            doctor_id,
            appointment_date,
            appointment_time,
            datetime.now().isoformat()
        )
    )

    connection.execute(
        """
        UPDATE slots
        SET available = 0
        WHERE id = ?
        """,
        (slot["id"],)
    )

    connection.commit()

    appointment_id = connection.execute(
        "SELECT last_insert_rowid()"
    ).fetchone()[0]

    connection.close()

    return {
        "success": True,
        "appointment": {
            "appointment_id": appointment_id,
            "patient_name": patient_name,
            "date": appointment_date,
            "time": appointment_time,
            "status": "Confirmed"
        }
    }