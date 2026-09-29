from database import (
    get_doctors,
    get_available_slots,
    book_appointment
)

from rag import HospitalRAG


# ==========================================
# 1. REQUIREMENT AGENT
# ==========================================

class RequirementAgent:

    def __init__(self):
        self.rag = HospitalRAG()

    def analyze(
        self,
        complaint,
        preferred_date,
        preferred_time
    ):

        text = complaint.lower()

        department_keywords = {

            "Cardiology": [
                "heart",
                "cardiac",
                "chest",
                "blood pressure",
                "bp"
            ],

            "Dermatology": [
                "skin",
                "rash",
                "acne",
                "itching",
                "hair"
            ],

            "Dentistry": [
                "tooth",
                "teeth",
                "dental",
                "gum"
            ],

            "Orthopedics": [
                "bone",
                "joint",
                "knee",
                "back pain",
                "fracture"
            ],

            "Neurology": [
                "headache",
                "migraine",
                "nerve",
                "memory"
            ],

            "General Medicine": [
                "fever",
                "cold",
                "cough",
                "checkup",
                "general"
            ]
        }

        detected_department = "General Medicine"

        for department, keywords in department_keywords.items():

            for keyword in keywords:

                if keyword in text:

                    detected_department = department
                    break

            if detected_department == department:
                break

        return {

            "original_request": complaint,

            "detected_department":
                detected_department,

            "preferred_date":
                preferred_date,

            "preferred_time":
                preferred_time
        }


# ==========================================
# 2. DOCTOR / DEPARTMENT AGENT
# ==========================================

class DoctorDepartmentAgent:

    def recommend(self, requirements):

        department = requirements[
            "detected_department"
        ]

        doctors = get_doctors()

        matching_doctors = [

            doctor

            for doctor in doctors

            if doctor["department"] == department
        ]

        return {

            "department": department,

            "doctors": matching_doctors,

            "reason":
                f"The patient's request was mapped "
                f"to the {department} department."
        }


# ==========================================
# 3. AVAILABILITY AGENT
# ==========================================

class AvailabilityAgent:

    def find_slots(
        self,
        doctor_id,
        appointment_date
    ):

        return get_available_slots(
            doctor_id,
            appointment_date
        )


# ==========================================
# 4. SCHEDULING AGENT
# ==========================================

class SchedulingAgent:

    def schedule(
        self,
        patient_name,
        phone,
        doctor_id,
        appointment_date,
        appointment_time
    ):

        return book_appointment(

            patient_name,

            phone,

            doctor_id,

            appointment_date,

            appointment_time
        )