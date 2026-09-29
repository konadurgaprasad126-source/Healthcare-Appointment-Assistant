# 🏥 Healthcare Appointment Assistant

An AI-powered healthcare appointment assistant built with **Python** and
**Streamlit**. The application helps users find relevant hospital
departments and doctors, access hospital information, and manage
appointments through an interactive web interface.

## 📌 Project Overview

The Healthcare Appointment Assistant combines:

-   **Streamlit** for the web interface
-   **Python** for application logic
-   **AI Agent logic** for doctor/department recommendations
-   **RAG (Retrieval-Augmented Generation)** for retrieving information
    from hospital documents
-   **SQLite** for storing appointment information

The system is designed to make the appointment process easier by
allowing users to interact with hospital information and receive
relevant recommendations.

## ✨ Features

### 👨‍⚕️ Doctor / Department Recommendation

The application includes a Doctor / Department Agent that can recommend
a suitable hospital department and display doctors associated with the
recommended department.

### 📚 RAG-Based Hospital Information

The application uses hospital-specific text documents as a knowledge
source:

-   `hospital_services.txt`
-   `hospital_policies.txt`
-   `appointment_faq.txt`

RAG helps the system retrieve relevant information from these documents
when answering hospital-related questions.

### 📅 Appointment Management

Users can select appointment information such as:

-   Department
-   Doctor
-   Appointment date
-   Appointment time

Appointment information can be stored in the SQLite database.

### 🗄️ Database

The project uses SQLite through the `appointments.db` database file.
Database-related operations are handled by `database.py`.

### 🖥️ Interactive Web Interface

The application is built using Streamlit, providing interactive
components such as buttons, text fields, selections, date inputs,
warnings, and result displays.

------------------------------------------------------------------------

## 🛠️ Technologies Used

  Technology                   Purpose
  ---------------------------- --------------------------------------------
  Python                       Main programming language
  Streamlit                   Web application/interface
  RAG                          Retrieval of hospital-specific information
  AI Agents                    Department/doctor recommendation
  SQLite                       Appointment data storage
  VS Code                      Development environment
  Python Virtual Environment   Dependency isolation

------------------------------------------------------------------------

## 📁 Project Structure

``` text
Healthcare-Appointment-Assistant/
│
├── app.py
├── agents.py
├── rag.py
├── database.py
├── appointments.db
│
├── data/
│   ├── appointment_faq.txt
│   ├── hospital_policies.txt
│   └── hospital_services.txt
│
└── venv/
```

### File Description

#### `app.py`

Main Streamlit application. It controls the user interface and connects
the different parts of the project.

#### `agents.py`

Contains the AI-agent logic used for tasks such as department and doctor
recommendations.

#### `rag.py`

Contains the Retrieval-Augmented Generation functionality used to
retrieve relevant information from the hospital knowledge documents.

#### `database.py`

Contains database-related functions for creating, storing, and
retrieving appointment information.

#### `appointments.db`

SQLite database used to store appointment-related records.

#### `data/hospital_services.txt`

Contains information about hospital services and departments.

#### `data/hospital_policies.txt`

Contains hospital policies and related information.

#### `data/appointment_faq.txt`

Contains frequently asked questions related to appointments.

------------------------------------------------------------------------

## 🔄 Application Workflow

``` text
                User
                  │
                  ▼
        Streamlit Web Interface
                  │
                  ▼
              app.py
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
   AI Agent                RAG
   agents.py              rag.py
        │                   │
        ▼                   ▼
Department/Doctor     Hospital Documents
Recommendation        ├─ Services
        │             ├─ Policies
        │             └─ FAQs
        └─────────┬─────────┘
                  ▼
        Appointment Selection
                  │
                  ▼
             database.py
                  │
                  ▼
          appointments.db
```

## 🚀 Installation and Setup

### 1. Clone or download the project

Open the project folder in VS Code.

### 2. Create a virtual environment

On Windows PowerShell:

``` powershell
python -m venv venv
```

### 3. Activate the virtual environment

``` powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell does not allow script execution, use an appropriate
Python/terminal environment or adjust the execution policy according to
your system settings.

### 4. Install the required packages

If the project contains a `requirements.txt` file:

``` powershell
pip install -r requirements.txt
```

Otherwise, install the packages required by the project, including
Streamlit and any AI/RAG libraries used in the Python files.

### 5. Run the application

From the project root directory:

``` powershell
streamlit run app.py
```

Streamlit will provide a local URL, normally similar to:

``` text
http://localhost:8501
```

Open that URL in your browser.

------------------------------------------------------------------------

## 💡 How to Use

1.  Start the Streamlit application.
2.  Enter the required healthcare/appointment information.
3.  Use the Doctor / Department Agent to obtain a department
    recommendation.
4.  Review the available doctors.
5.  Select the required doctor.
6.  Select an available appointment date and time.
7.  Submit the appointment.
8.  Appointment information is stored in the SQLite database.

For hospital information questions, the RAG component can retrieve
information from the documents in the `data` folder.

------------------------------------------------------------------------
