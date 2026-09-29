import streamlit as st
from datetime import date

from database import init_db
from agents import (
    RequirementAgent,
    DoctorDepartmentAgent,
    AvailabilityAgent,
    SchedulingAgent
)
from rag import HospitalRAG


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Healthcare Appointment Assistant",
    page_icon="🏥",
    layout="wide"
)

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #eaf4ff 0%, #ffffff 55%, #f4faff 100%);
    }

    [data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.82);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #dceeff 0%, #f8fcff 100%);
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INITIALIZE DATABASE
# =========================================================

init_db()


# =========================================================
# INITIALIZE AGENTS
# =========================================================

requirement_agent = RequirementAgent()
doctor_agent = DoctorDepartmentAgent()
availability_agent = AvailabilityAgent()
scheduling_agent = SchedulingAgent()

hospital_rag = HospitalRAG()


# =========================================================
# SESSION STATE
# =========================================================

if "requirements" not in st.session_state:
    st.session_state.requirements = None

if "doctor_results" not in st.session_state:
    st.session_state.doctor_results = None

if "booking_result" not in st.session_state:
    st.session_state.booking_result = None


# =========================================================
# HEADER
# =========================================================

st.title("🏥 Healthcare Appointment Assistant")

st.write(
    "A simulated multi-agent healthcare appointment "
    "system built using Python and Streamlit."
)

st.info(
    "This is an educational simulation. "
    "It does not provide medical diagnosis or emergency care."
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🤖 AI Agents")

    st.write("The system uses four specialized agents:")

    st.markdown(
        """
        **1. Requirement Agent**  
        Understands the patient's request.

        **2. Doctor/Department Agent**  
        Identifies the suitable department and doctors.

        **3. Availability Agent**  
        Checks available appointment slots.

        **4. Scheduling Agent**  
        Books the selected appointment.
        """
    )

    st.divider()

    st.header("📚 RAG Knowledge Base")

    st.write(
        "Hospital policies, services, and appointment "
        "information are retrieved from the local knowledge base."
    )


# =========================================================
# MAIN TABS
# =========================================================

tab1, tab2 = st.tabs(
    [
        "📅 Book Appointment",
        "📚 Hospital Information"
    ]
)


# =========================================================
# TAB 1 - APPOINTMENT
# =========================================================

with tab1:

    st.header("Book a Healthcare Appointment")

    st.write(
        "Enter your requirements and the agents will "
        "help identify a department, doctor, and available slot."
    )

    # -----------------------------------------------------
    # PATIENT DETAILS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        patient_name = st.text_input(
            "Patient Name",
            placeholder="Enter patient name"
        )

    with col2:

        phone = st.text_input(
            "Phone Number",
            placeholder="Enter phone number"
        )

    # -----------------------------------------------------
    # REQUIREMENT
    # -----------------------------------------------------

    complaint = st.text_area(
        "Describe your requirement",
        placeholder=(
            "Example: I have a skin problem and want "
            "to consult a doctor."
        ),
        height=100
    )

    # -----------------------------------------------------
    # DATE
    # -----------------------------------------------------

    preferred_date = st.date_input(
        "Preferred Appointment Date",
        min_value=date(1998, 1, 1),
        max_value=date(2030, 12, 31),
        value=date.today()
    )

    # -----------------------------------------------------
    # ANALYZE BUTTON
    # -----------------------------------------------------

    if st.button(
        "🔎 Analyze Requirement",
        use_container_width=True
    ):

        if not complaint.strip():

            st.warning(
                "Please describe your requirement first."
            )

        else:

            requirements = requirement_agent.analyze(
                complaint,
                str(preferred_date),
                ""
            )

            st.session_state.requirements = requirements

            doctor_results = doctor_agent.recommend(
                requirements
            )

            st.session_state.doctor_results = doctor_results

            st.session_state.booking_result = None


    # =====================================================
    # DISPLAY REQUIREMENT ANALYSIS
    # =====================================================

    if st.session_state.requirements:

        requirements = st.session_state.requirements

        st.divider()

        st.subheader("🤖 Requirement Agent")

        st.success(
            "Requirement analyzed successfully."
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Patient Requirement:**")

            st.write(
                requirements["original_request"]
            )

        with col2:

            st.write("**Detected Department:**")

            st.info(
                requirements["detected_department"]
            )


    # =====================================================
    # DISPLAY DOCTORS
    # =====================================================

    if st.session_state.doctor_results:

        doctor_results = st.session_state.doctor_results

        st.divider()

        st.subheader("👨‍⚕️ Doctor / Department Agent")

        st.write(
            f"Recommended Department: "
            f"**{doctor_results['department']}**"
        )

        doctors = doctor_results["doctors"]

        if not doctors:

            st.warning(
                "No doctors were found for this department."
            )

        else:

            doctor_options = {
                (
                    f"{doctor['name']} — "
                    f"{doctor['department']} "
                    f"({doctor['experience']} years experience)"
                ):
                doctor["id"]

                for doctor in doctors
            }

            selected_doctor_name = st.selectbox(
                "Select Doctor",
                list(doctor_options.keys())
            )

            selected_doctor_id = doctor_options[
                selected_doctor_name
            ]

            # =================================================
            # AVAILABILITY AGENT
            # =================================================

            st.divider()

            st.subheader("🕐 Availability Agent")

            selected_date = st.date_input(
                "Select Appointment Date",
                min_value=date.today(),
                value=max(preferred_date, date.today()),
                key="appointment_date"
            )

            selected_date_string = str(
                selected_date
            )

            available_slots = (
                availability_agent.find_slots(
                    selected_doctor_id,
                    selected_date_string
                )
            )

            if not available_slots:

                st.warning(
                    "No available slots for this doctor "
                    "on the selected date."
                )

            else:

                slot_options = [
                    slot["appointment_time"]
                    for slot in available_slots
                ]

                selected_time = st.selectbox(
                    "Select Available Time",
                    slot_options
                )

                # =============================================
                # SCHEDULING AGENT
                # =============================================

                st.divider()

                st.subheader("📅 Scheduling Agent")

                if st.button(
                    "✅ Confirm Appointment",
                    use_container_width=True
                ):

                    if not patient_name.strip():

                        st.error(
                            "Please enter the patient name."
                        )

                    elif not phone.strip():

                        st.error(
                            "Please enter the phone number."
                        )

                    else:

                        booking = (
                            scheduling_agent.schedule(
                                patient_name,
                                phone,
                                selected_doctor_id,
                                selected_date_string,
                                selected_time
                            )
                        )

                        st.session_state.booking_result = booking


    # =====================================================
    # BOOKING RESULT
    # =====================================================

    if st.session_state.booking_result:

        result = st.session_state.booking_result

        st.divider()

        if result["success"]:

            appointment = result["appointment"]

            st.success(
                "🎉 Appointment booked successfully!"
            )

            st.subheader(
                "Appointment Confirmation"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Appointment ID:** "
                    f"{appointment['appointment_id']}"
                )

                st.write(
                    f"**Patient:** "
                    f"{appointment['patient_name']}"
                )

                st.write(
                    f"**Date:** "
                    f"{appointment['date']}"
                )

            with col2:

                st.write(
                    f"**Time:** "
                    f"{appointment['time']}"
                )

                st.write(
                    f"**Status:** "
                    f"{appointment['status']}"
                )

        else:

            st.error(
                result["message"]
            )


# =========================================================
# TAB 2 - RAG HOSPITAL INFORMATION
# =========================================================

with tab2:

    st.header("📚 Hospital Information")

    st.write(
        "Ask questions about hospital policies, "
        "services, and appointment procedures."
    )

    question = st.text_input(
        "Ask a question",
        placeholder=(
            "Example: How early should I arrive "
            "for my appointment?"
        )
    )

    if st.button(
        "🔍 Search Hospital Information",
        use_container_width=True
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            rag_result = hospital_rag.answer(
                question
            )

            st.subheader("📖 RAG Answer")

            st.markdown(
                rag_result["answer"]
            )

            if rag_result["sources"]:

                st.subheader(
                    "📄 Retrieved Sources"
                )

                for source in rag_result["sources"]:

                    st.write(
                        f"• {source['title']}"
                    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Healthcare Appointment Assistant | "
    "Python + Streamlit + Multi-Agent System + RAG"
)