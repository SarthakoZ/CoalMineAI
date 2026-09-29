# ⛏️ CoalMineAI

### AI-Powered Coal Mine Safety, Compliance & Operational Intelligence Platform

CoalMineAI is a software-based AI platform designed to centralize coal mine inspections, safety monitoring, compliance analysis, workforce information, operational data, and AI-powered risk prediction into a single command-center dashboard.

The platform combines **Python, PostgreSQL, Scikit-learn, Random Forest, Pandas, Joblib, and Streamlit**.

## 🚀 Live Demo

[CoalMineAI Live Demo](https://coalmineai-4acz5g5zld5k5sz9ubnkia.streamlit.app/)

## 🚀 Overview

```text
Inspector
   ↓
Inspection Data Entry
   ↓
PostgreSQL Database
   ↓
Data Processing
   ↓
Random Forest ML Model
   ↓
Compliance Risk Prediction
   ↓
Prediction Database
   ↓
CoalMineAI Command Center
```

---

## ✨ Features

### 🖥️ Command Center
- Centralized mine monitoring
- Mine status
- Latest inspection information
- Environmental monitoring
- Workforce information
- Attendance monitoring
- Production monitoring
- Inspection score
- AI compliance risk
- Prediction confidence
- Prediction history

### 🛡️ Safety Intelligence
- Methane percentage
- CO concentration
- Temperature
- Humidity
- Helmet compliance
- PPE compliance
- Equipment condition
- Safety observation level
- Previous violations
- Contractor compliance
- Emergency equipment status
- Inspection score

### 🤖 AI Compliance Prediction

CoalMineAI uses a trained **Random Forest Classifier** to predict compliance risk.

```text
Raw Inspection Data
        ↓
Missing Value Handling
        ↓
Numerical Scaling
        ↓
Categorical Encoding
        ↓
Random Forest Classifier
        ↓
Compliance Risk
        ↓
Prediction Probability
```

Each prediction stores:

- Inspection ID
- Compliance risk
- Prediction probability
- Model version
- Prediction timestamp

### 📋 Inspector Data Entry

Inspectors can submit:

- Mine ID
- Inspection date and time
- Location
- Methane
- CO
- Temperature
- Humidity
- Worker count
- Attendance
- Helmet compliance
- PPE compliance
- Equipment condition
- Safety observation level
- Previous violations
- Contractor compliance
- Emergency equipment status
- Inspection score
- Production tonnes

### 👷 Workforce Intelligence
- Worker records
- Contractor information
- Attendance percentage
- Worker count

### ⚙️ Equipment Intelligence
- Equipment records
- Equipment condition
- Operational information

### 🛰️ Visual Monitoring

| Module | Purpose |
|---|---|
| 🌡️ Thermal | Thermal mine visualization |
| 🌙 Night Vision | Low-light visualization |
| 🗺️ GIS | Mine/location visualization |

---

# 🖥️ Command Center

```text
┌─────────────────────────────────────────────┐
│          COALMINEAI COMMAND CENTER          │
├─────────────────────────────────────────────┤
│ Mine Status │ AI Risk │ Inspection │ Workers│
├─────────────────────────────────────────────┤
│     THERMAL │ NIGHT VISION │ GIS            │
├─────────────────────────────────────────────┤
│              SYSTEM OVERVIEW                │
├─────────────────────────────────────────────┤
│ Environmental │ Safety │ Workforce │ Output │
├─────────────────────────────────────────────┤
│          AI COMPLIANCE INTELLIGENCE         │
├─────────────────────────────────────────────┤
│              INSPECTION DATA                │
└─────────────────────────────────────────────┘
```

---

# 🧠 Machine Learning

### Model

```text
Algorithm: Random Forest Classifier
```

### Input Features

```text
location
methane_percent
co_ppm
temperature_c
humidity_percent
worker_count
attendance_percent
helmet_compliance
ppe_compliance
equipment_condition
safety_observation_level
previous_violations
contractor_compliance
emergency_equipment_ok
inspection_score
production_tonnes
```

### Preprocessing

**Numerical features**
- SimpleImputer
- StandardScaler

**Categorical features**
- SimpleImputer
- OneHotEncoder

The preprocessing and Random Forest classifier are combined into a single Scikit-learn pipeline.

---

# 📊 ML Architecture

```text
                  INSPECTION DATA
                         ↓
                    PREPROCESS
                         ↓
              ┌──────────┴──────────┐
              ↓                     ↓
       Numerical Data       Categorical Data
              ↓                     ↓
         Imputation             Imputation
              ↓                     ↓
           Scaling               Encoding
              └──────────┬──────────┘
                         ↓
                  Random Forest
                         ↓
                 Compliance Risk
                         ↓
                Prediction Probability
```

---

# 🗄️ PostgreSQL Database

CoalMineAI uses PostgreSQL as its primary database.

Main data areas:

```text
mines
inspections
predictions
workers
equipment
```

### Inspections

```text
inspection_id
mine_id
inspection_date
inspection_time
location
methane_percent
co_ppm
temperature_c
humidity_percent
worker_count
attendance_percent
helmet_compliance
ppe_compliance
equipment_condition
safety_observation_level
previous_violations
contractor_compliance
emergency_equipment_ok
inspection_score
production_tonnes
```

### Predictions

```text
prediction_id
inspection_id
compliance_risk
prediction_probability
model_version
predicted_at
```

---

# 📁 Project Structure

```text
CoalMineAI/
│
├── app.py
├── database.py
├── predict.py
├── training.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── models/
│   └── mineshield_compliance_model.pkl
│
├── images/
│   ├── Thermal.jpg
│   ├── Night_Vision.jpg
│   └── GIS.jpg
│
└── __pycache__/
```

---

# 🛠️ Technology Stack

### Programming
- Python

### Machine Learning
- Scikit-learn
- Random Forest
- Pandas
- NumPy
- Joblib

### Database
- PostgreSQL
- Psycopg2
- pgAdmin

### Dashboard
- Streamlit

### Development
- VS Code
- Git
- GitHub
- PowerShell

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/CoalMineAI.git
cd CoalMineAI
```

## 2. Create Virtual Environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Ubuntu / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄️ PostgreSQL Setup

Create the database:

```sql
CREATE DATABASE "CoalMineAI";
```

Required configuration:

```text
Host     : localhost
Database : CoalMineAI
User     : postgres
Port     : 5432
```

Make sure PostgreSQL is running before starting CoalMineAI.

---

# 🔐 Security

Do not commit database passwords or other credentials to GitHub.

Use:

```text
.streamlit/secrets.toml
```

Example:

```toml
[postgres]
host = "localhost"
database = "CoalMineAI"
user = "postgres"
password = "YOUR_PASSWORD"
port = "5432"
```

Make sure the secrets file is included in `.gitignore`.

For production, use environment variables or your deployment platform's secret-management system.

---

# ▶️ Running CoalMineAI

From the project directory:

```powershell
cd D:\CoalMineAI
```

Start the dashboard:

```powershell
streamlit run app.py
```

---

# 🔮 Prediction Workflow

```text
Inspector opens CoalMineAI
          ↓
Inspector enters inspection data
          ↓
Data inserted into PostgreSQL
          ↓
Inspection ID generated
          ↓
ML pipeline loads inspection
          ↓
Random Forest generates prediction
          ↓
Prediction probability calculated
          ↓
Prediction stored in PostgreSQL
          ↓
Dashboard displays result
```

---

# 📈 Prediction Example

```text
┌──────────────────────────────────────┐
│       AI COMPLIANCE PREDICTION       │
├──────────────────────────────────────┤
│ Inspection ID       : 1              │
│ Risk                : LOW            │
│ Confidence          : 83.00%         │
│ Model               : Random Forest  │
│ Version             : v1             │
└──────────────────────────────────────┘
```

---

# 📊 Dashboard Sections

```text
COMMAND CENTER
      │
      ├── Safety Intelligence
      ├── AI Compliance
      ├── Inspector Entry
      ├── Workforce
      ├── Equipment
      ├── Visual Monitoring
      │      ├── Thermal
      │      ├── Night Vision
      │      └── GIS
      └── Inspection History
```

---

# 🧪 Testing

### Test Database Connection

```powershell
python database.py
```

Expected:

```text
Database connected successfully!
```

### Test Prediction

```powershell
python predict.py
```

### Test Dashboard

```powershell
streamlit run app.py
```

---

# 📦 Requirements

Core dependencies:

```text
streamlit
pandas
psycopg2-binary
scikit-learn
joblib
numpy
```

---

# 🔒 Git & Security

Do not commit:

```text
.streamlit/secrets.toml
.env
venv/
__pycache__/
*.log
```

Never expose:

```text
Database passwords
API keys
Secret tokens
Production credentials
```

---

# 🎯 Project Objective

CoalMineAI is designed to provide a centralized software platform for mine safety and compliance intelligence.

The system converts structured inspection information into machine-learning-based compliance insights while keeping the workflow simple for inspectors and dashboard users.

```text
COLLECT
   ↓
STORE
   ↓
PROCESS
   ↓
PREDICT
   ↓
MONITOR
```

---

# 🔭 Future Scope

- Real-time sensor integration
- Advanced risk analytics
- Automated compliance reports
- Mine-wise analytics
- Historical risk trends
- Automated alerts
- Role-based authentication
- Cloud deployment
- Advanced GIS integration
- Automated inspection reports
- Additional machine-learning models
- Real-time operational monitoring

---

# 💡 Why CoalMineAI?

CoalMineAI brings multiple mine-management functions into a single software platform:

```text
        ┌──────────────────────┐
        │      CoalMineAI      │
        └──────────┬───────────┘
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
    SAFETY       AI RISK     OPERATIONS
       │           │           │
       ↓           ↓           ↓
  Inspection   Prediction   Production
  Monitoring   Analytics    Workforce
       │           │           │
       └───────────┼───────────┘
                   ↓
            COMMAND CENTER
```

---

# 👨‍💻 Developer

## Sarthak Ruidas

**B.Tech CSE (AI & ML)**

Interests:

```text
Machine Learning
Artificial Intelligence
Python
Data Science
Software Development
```

---

# ⭐ CoalMineAI

If you find **CoalMineAI** interesting, consider starring the repository on GitHub.

```text
╔══════════════════════════════════════════════╗
║                 COALMINEAI                   ║
║                                              ║
║       AI-POWERED MINE INTELLIGENCE           ║
║                                              ║
║         COLLECT → PREDICT → MONITOR          ║
╚══════════════════════════════════════════════╝
```

### ⛏️ Collect. Analyze. Predict. Monitor.
