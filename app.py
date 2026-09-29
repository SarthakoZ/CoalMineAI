import html
import logging
import os
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

from database import get_connection

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("coalmineai")

st.set_page_config(page_title="CoalMineAI Command Center", page_icon="⛏️",
                   layout="wide", initial_sidebar_state="expanded")

# ---------------------------------------------------------------- config
# Override with environment variables; defaults are relative to this file
# (no hard-coded D:\ paths).
BASE_DIR = Path(os.getenv("COALMINEAI_HOME", Path(__file__).resolve().parent))
MODEL_PATH = Path(os.getenv("COALMINEAI_MODEL", BASE_DIR / "model" / "mineshield_compliance_model.pkl"))
IMAGES = {
    "THERMAL MONITORING": BASE_DIR / "images" / "Thermal.jpg",
    "NIGHT VISION": BASE_DIR / "images" / "Night_Vision.jpg",
    "GIS MINE MAP": BASE_DIR / "images" / "GIS.jpg",
}
MODEL_VERSION = "Random Forest v1"
TABLE_ROW_LIMIT = 1000

FEATURE_COLUMNS = [
    "location", "methane_percent", "co_ppm", "temperature_c", "humidity_percent",
    "worker_count", "attendance_percent", "helmet_compliance", "ppe_compliance",
    "equipment_condition", "safety_observation_level", "previous_violations",
    "contractor_compliance", "emergency_equipment_ok", "inspection_score",
    "production_tonnes",
]
INSPECTION_COLUMNS = ["mine_id", "inspection_date", "inspection_time"] + FEATURE_COLUMNS

RISK_COLORS = {"LOW": "#45e8bc", "MEDIUM": "#ffd166", "HIGH": "#ff6678"}

# ---------------------------------------------------------------- styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: radial-gradient(circle at 10% 0%, rgba(0,220,180,.08), transparent 25%),
  radial-gradient(circle at 90% 10%, rgba(0,170,255,.07), transparent 25%), #070b10; color:#e8edf2; }
.block-container { max-width:1500px; padding-top:2rem; padding-bottom:3rem; }
section[data-testid="stSidebar"] { background:#080d13; border-right:1px solid rgba(0,255,200,.12); }
section[data-testid="stSidebar"] > div { padding-top:2rem; }
section[data-testid="stSidebar"] .stRadio label { color:#9daab7; }
section[data-testid="stSidebar"] .stRadio label:hover { color:#00f5c3; }
h1,h2,h3 { color:#f2f7fa !important; letter-spacing:-.5px; font-weight:700 !important; }
.stButton > button, .stFormSubmitButton > button { background:linear-gradient(135deg,#00cfa5,#00a6ff);
  color:#041016; border:none; border-radius:10px; font-weight:800; min-height:48px; transition:all .2s ease; }
.stButton > button:hover, .stFormSubmitButton > button:hover { transform:translateY(-2px);
  box-shadow:0 8px 30px rgba(0,220,180,.22); }
.stTextInput input, .stNumberInput input, .stDateInput input, .stTimeInput input {
  background:#0c131b !important; color:#edf5f7 !important; border:1px solid #263542 !important; border-radius:8px !important; }
div[data-baseweb="select"] > div { background:#0c131b !important; border-color:#263542 !important; color:#edf5f7 !important; }
[data-testid="stMetric"] { background:linear-gradient(145deg,rgba(16,25,34,.95),rgba(9,15,21,.95));
  border:1px solid rgba(0,220,180,.13); border-radius:14px; padding:18px; box-shadow:0 8px 30px rgba(0,0,0,.22); }
[data-testid="stMetricLabel"] { color:#7f919f !important; }
[data-testid="stMetricValue"] { color:#eaf8f5 !important; font-family:'Space Mono',monospace; }
.stDataFrame { border:1px solid #1c2b37; border-radius:12px; }
hr { border-color:#1c2933 !important; }
.command-header { padding:25px 28px; border-radius:18px; margin-bottom:22px;
  background:linear-gradient(135deg,rgba(0,212,170,.10),rgba(0,125,255,.06));
  border:1px solid rgba(0,220,180,.18); box-shadow:0 15px 50px rgba(0,0,0,.25); }
.command-title { font-size:32px; font-weight:800; letter-spacing:1px; color:#f5fbfd; }
.command-subtitle { margin-top:5px; color:#8194a1; font-size:14px; }
.status-pill { display:inline-flex; align-items:center; gap:8px; background:rgba(0,220,160,.08);
  border:1px solid rgba(0,220,160,.25); padding:7px 13px; border-radius:30px; color:#48efc4; font-size:12px; font-weight:700; }
.status-pill.down { background:rgba(255,102,120,.08); border-color:rgba(255,102,120,.3); color:#ff6678; }
.status-dot { width:8px; height:8px; background:currentColor; border-radius:50%; box-shadow:0 0 12px currentColor; }
.section-label { color:#00dfb3; font-size:11px; font-family:'Space Mono',monospace; letter-spacing:2px; margin-bottom:8px; }
.monitor-title { display:flex; justify-content:space-between; padding:6px 10px; border-radius:7px 7px 0 0;
  background:#0b1219; border:1px solid #20303b; border-bottom:none; color:#fff; font-size:11px; font-weight:700; letter-spacing:1px; }
.monitor-title span { color:#4bf0c5; font-family:'Space Mono',monospace; font-size:10px; }
.monitor-missing { min-height:160px; display:flex; align-items:center; justify-content:center; border:1px dashed #20303b;
  border-radius:0 0 12px 12px; color:#53636f; font-size:12px; }
.ai-panel { background:radial-gradient(circle at 85% 20%,rgba(0,220,180,.12),transparent 30%),#0b131b;
  border:1px solid rgba(0,220,180,.22); border-radius:18px; padding:25px; box-shadow:0 15px 50px rgba(0,0,0,.28); }
.ai-title { font-family:'Space Mono',monospace; color:#7f909c; font-size:11px; letter-spacing:2px; }
.ai-risk { font-size:42px; font-weight:800; margin-top:8px; }
.ai-probability { color:#9baab5; font-family:'Space Mono',monospace; font-size:13px; }
.info-card { background:#0b131b; border:1px solid #1c2d38; border-radius:15px; padding:20px; height:100%; }
.info-value { color:#e9f5f5; font-size:23px; font-weight:700; }
.info-label { color:#718491; font-size:11px; text-transform:uppercase; letter-spacing:1px; }
.alert-card { border-radius:12px; padding:13px 16px; margin:7px 0; background:#0d151d; border:1px solid #1c2b35; }
.footer { margin-top:40px; padding-top:18px; border-top:1px solid #17242d; color:#53636f;
  font-family:'Space Mono',monospace; font-size:10px; text-align:center; }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------- helpers
def esc(value) -> str:
    """HTML-escape anything that goes into unsafe_allow_html markup."""
    return html.escape(str(value))


def label(text: str):
    st.markdown(f'<div class="section-label">{esc(text)}</div>', unsafe_allow_html=True)


def spacer():
    st.markdown("<br>", unsafe_allow_html=True)


def normalize_risk(value) -> str:
    return str(value).strip().upper() if value is not None else "NO DATA"


@contextmanager
def db_cursor(commit: bool = False):
    """Always closes the connection; rolls back on error."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            yield cur
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_data(query: str, params=None) -> pd.DataFrame:
    """Run a read query. Returns an empty DataFrame (and shows an error) on failure."""
    try:
        with db_cursor() as cur:
            cur.execute(query, params or ())
            rows = cur.fetchall()
            columns = [d[0] for d in cur.description]
        return pd.DataFrame(rows, columns=columns)
    except Exception:
        log.exception("Query failed: %s", query.strip()[:120])
        st.error("Database error: could not load data. Check the connection and try again.")
        return pd.DataFrame()


def get_scalar(query: str, default=0):
    df = get_data(query)
    return default if df.empty else df.iloc[0, 0]


@st.cache_resource(show_spinner=False)
def load_model():
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


def db_healthy() -> bool:
    try:
        with db_cursor() as cur:
            cur.execute("SELECT 1")
        return True
    except Exception:
        log.exception("Database health check failed")
        return False


def predict_risk(data: dict):
    """Pure prediction step: no DB writes, so a model failure never leaves orphan rows."""
    model = load_model()
    cols = list(getattr(model, "feature_names_in_", FEATURE_COLUMNS))
    missing = [c for c in cols if c not in data]
    if missing:
        raise ValueError(f"Model expects features not provided: {missing}")
    features = pd.DataFrame([[data[c] for c in cols]], columns=cols)
    prediction = str(model.predict(features)[0])
    probability = float(model.predict_proba(features).max()) if hasattr(model, "predict_proba") else 0.0
    return prediction, probability


def save_inspection_with_prediction(data: dict, prediction: str, probability: float) -> int:
    """Insert inspection + prediction in ONE transaction (all or nothing)."""
    placeholders = ", ".join(["%s"] * len(INSPECTION_COLUMNS))
    insert_inspection = (f"INSERT INTO inspections ({', '.join(INSPECTION_COLUMNS)}) "
                         f"VALUES ({placeholders}) RETURNING inspection_id")
    with db_cursor(commit=True) as cur:
        cur.execute(insert_inspection, tuple(data[c] for c in INSPECTION_COLUMNS))
        inspection_id = int(cur.fetchone()[0])
        cur.execute(
            "INSERT INTO predictions (inspection_id, compliance_risk, prediction_probability, model_version) "
            "VALUES (%s, %s, %s, %s)",
            (inspection_id, prediction, probability, MODEL_VERSION),
        )
    return inspection_id


def validate_inspection(d: dict) -> list:
    errors = []
    if not d["location"]:
        errors.append("Inspection location is required.")
    if len(d["location"]) > 200:
        errors.append("Location must be 200 characters or fewer.")
    if d["inspection_date"] > date.today():
        errors.append("Inspection date cannot be in the future.")
    if d["worker_count"] <= 0:
        errors.append("Worker count must be greater than zero.")
    if d["methane_percent"] > 100:
        errors.append("Methane cannot exceed 100%.")
    if not -50 <= d["temperature_c"] <= 100:
        errors.append("Temperature must be between -50 and 100 °C.")
    return errors


def ai_panel(risk: str, probability: float, footer: str):
    risk = normalize_risk(risk)
    color = RISK_COLORS.get(risk, "#9baab5")
    st.markdown(f"""
    <div class="ai-panel">
      <div class="ai-title">AI COMPLIANCE ASSESSMENT</div>
      <div class="ai-risk" style="color:{color};">{esc(risk)}</div>
      <div class="ai-probability">MODEL CONFIDENCE&nbsp;&nbsp;{probability * 100:.2f}%</div>
      <div style="margin-top:18px; color:#637581; font-size:12px;">{esc(footer)}</div>
    </div>""", unsafe_allow_html=True)


def info_card(title: str, value):
    st.markdown(f"""
    <div class="info-card"><div class="info-label">{esc(title)}</div>
    <div class="info-value">{esc(value)}</div></div>""", unsafe_allow_html=True)


def table_page(section: str, header: str, query: str, empty_msg: str):
    label(section)
    st.header(header)
    df = get_data(query)
    if df.empty:
        st.info(empty_msg)
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Showing up to {TABLE_ROW_LIMIT} most recent rows.")


def monitor(title: str, status: str, path: Path):
    st.markdown(f'<div class="monitor-title">{esc(title)}<span>{esc(status)}</span></div>', unsafe_allow_html=True)
    if path.is_file():
        try:
            st.image(str(path), use_container_width=True)
            return
        except Exception:
            log.exception("Could not render image %s", path)
    st.markdown('<div class="monitor-missing">FEED UNAVAILABLE</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------- header
db_ok = db_healthy()
pill = ('<div class="status-pill"><span class="status-dot"></span>SYSTEM OPERATIONAL</div>' if db_ok else
        '<div class="status-pill down"><span class="status-dot"></span>DATABASE OFFLINE</div>')
st.markdown(f"""
<div class="command-header"><div style="display:flex; justify-content:space-between; align-items:center;">
  <div><div class="section-label">AI SAFETY INTELLIGENCE PLATFORM</div>
  <div class="command-title">COALMINEAI COMMAND CENTER</div>
  <div class="command-subtitle">Centralized mine safety, compliance and operational intelligence</div></div>
  {pill}
</div></div>""", unsafe_allow_html=True)

if not db_ok:
    st.error("Cannot reach the database. Verify PostgreSQL is running and credentials in database.py are correct.")
    if st.button("Retry connection"):
        st.rerun()
    st.stop()

menu = st.sidebar.radio("COMMAND CENTER",
                        ["Dashboard", "Inspector Data Entry", "Inspections", "Predictions", "Workers", "Equipment"])


# ---------------------------------------------------------------- pages
def page_dashboard():
    label("LIVE MONITORING")
    cols = st.columns(3)
    for col, (title, path), status in zip(cols, IMAGES.items(), ["● LIVE", "● LIVE", "● ACTIVE"]):
        with col:
            monitor(title, status, path)
    spacer()

    label("SYSTEM TELEMETRY")
    risk_counts = get_data("SELECT compliance_risk, COUNT(*) AS n FROM predictions GROUP BY compliance_risk")
    counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
    for _, row in risk_counts.iterrows():
        key = normalize_risk(row["compliance_risk"])
        counts[key] = counts.get(key, 0) + int(row["n"])

    metrics = [
        ("ACTIVE MINES", get_scalar("SELECT COUNT(*) FROM mines")),
        ("WORKFORCE", get_scalar("SELECT COUNT(*) FROM workers")),
        ("EQUIPMENT", get_scalar("SELECT COUNT(*) FROM equipment")),
        ("INSPECTIONS", get_scalar("SELECT COUNT(*) FROM inspections")),
        ("HIGH RISK", counts["HIGH"]),
    ]
    for col, (name, value) in zip(st.columns(5), metrics):
        col.metric(name, int(value))
    spacer()

    latest_pred = get_data("SELECT compliance_risk, prediction_probability FROM predictions "
                           "ORDER BY prediction_id DESC LIMIT 1")
    if latest_pred.empty:
        risk, probability = "NO DATA", 0.0
    else:
        risk = latest_pred.iloc[0]["compliance_risk"]
        probability = float(latest_pred.iloc[0]["prediction_probability"] or 0)

    left, right = st.columns(2)
    with left:
        ai_panel(risk, probability, f"{MODEL_VERSION} · PostgreSQL Inspection Engine")
    with right:
        rows = "".join(
            f'<div class="alert-card"><span style="color:{RISK_COLORS[k]};">● {k} RISK</span>'
            f'<span style="float:right;">{counts[k]}</span></div>'
            for k in ("LOW", "MEDIUM", "HIGH"))
        st.markdown(f'<div class="info-card"><div class="section-label">RISK DISTRIBUTION</div>'
                    f'<div style="margin-top:10px;">{rows}</div></div>', unsafe_allow_html=True)
    spacer()

    recent = get_data("SELECT * FROM inspections ORDER BY inspection_id DESC LIMIT 5")
    if recent.empty:
        st.info("No inspections recorded yet.")
        return

    label("LATEST INSPECTION INTELLIGENCE")
    latest = recent.iloc[0]
    cards = [("METHANE", f'{latest["methane_percent"]} %'), ("CO LEVEL", f'{latest["co_ppm"]} ppm'),
             ("TEMPERATURE", f'{latest["temperature_c"]} °C'), ("WORKERS PRESENT", latest["worker_count"])]
    for col, (title, value) in zip(st.columns(4), cards):
        with col:
            info_card(title, value)
    spacer()
    label("RECENT ACTIVITY")
    st.dataframe(recent, use_container_width=True, hide_index=True)


def page_data_entry():
    label("FIELD OPERATIONS")
    st.header("Inspector Safety Observation")
    st.write("Submit a mine inspection. The trained ML model will automatically generate a compliance-risk prediction.")

    mine_df = get_data("SELECT mine_id, mine_name FROM mines ORDER BY mine_id")
    if mine_df.empty:
        st.error("No mines are available in the database.")
        return
    mine_options = dict(zip(mine_df["mine_name"], mine_df["mine_id"]))

    try:  # fail early and clearly if the model can't be loaded
        load_model()
    except Exception as exc:
        log.exception("Model load failed")
        st.error(f"The AI model is unavailable: {exc}")
        return

    yes_no = lambda a, b: (lambda x: a if x == 0 else b)
    # st.form: no rerun per keystroke, and the submit button can't be double-fired mid-run.
    with st.form("inspection_form", clear_on_submit=False):
        selected_mine = st.selectbox("Mine", list(mine_options.keys()))
        c1, c2 = st.columns(2)
        with c1:
            inspection_date = st.date_input("Inspection Date", value=date.today(), max_value=date.today())
            inspection_time = st.time_input("Inspection Time", value=datetime.now().time().replace(microsecond=0))
            location = st.text_input("Inspection Location", max_chars=200)
            methane = st.number_input("Methane (%)", 0.0, 100.0, 0.0, 0.01)
            co_ppm = st.number_input("CO (ppm)", 0.0, 10000.0, 0.0, 0.5)
            temperature = st.number_input("Temperature (°C)", -50.0, 100.0, 0.0, 0.5)
            humidity = st.number_input("Humidity (%)", 0.0, 100.0, 0.0, 1.0)
            workers = st.number_input("Worker Count", 0, 100000, 0, 1)
            attendance = st.number_input("Attendance (%)", 0.0, 100.0, 0.0, 0.5)
        with c2:
            helmet = st.selectbox("Helmet Compliance", [0, 1], format_func=yes_no("NON-COMPLIANT", "COMPLIANT"))
            ppe = st.selectbox("PPE Compliance", [0, 1], format_func=yes_no("NON-COMPLIANT", "COMPLIANT"))
            equipment = st.selectbox("Equipment Condition", [0, 1], format_func=yes_no("POOR", "GOOD"))
            level = st.selectbox("Safety Observation Level", [0, 1, 2],
                                 format_func=lambda x: {0: "NORMAL", 1: "WARNING", 2: "CRITICAL"}[x])
            prev_viol = st.number_input("Previous Violations", 0, 100000, 0, 1)
            contractor = st.selectbox("Contractor Compliance", [0, 1], format_func=yes_no("NON-COMPLIANT", "COMPLIANT"))
            emergency = st.selectbox("Emergency Equipment", [0, 1], format_func=yes_no("NOT OPERATIONAL", "OPERATIONAL"))
            score = st.number_input("Inspection Score", 0.0, 100.0, 0.0, 1.0)
            production = st.number_input("Production (tonnes)", 0.0, 10_000_000.0, 0.0, 100.0)
        submitted = st.form_submit_button("RUN INSPECTION & AI RISK ANALYSIS", type="primary",
                                          use_container_width=True)

    if not submitted:
        return

    data = {
        "mine_id": int(mine_options[selected_mine]), "inspection_date": inspection_date,
        "inspection_time": inspection_time, "location": location.strip(),
        "methane_percent": float(methane), "co_ppm": float(co_ppm), "temperature_c": float(temperature),
        "humidity_percent": float(humidity), "worker_count": int(workers),
        "attendance_percent": float(attendance), "helmet_compliance": int(helmet),
        "ppe_compliance": int(ppe), "equipment_condition": int(equipment),
        "safety_observation_level": int(level), "previous_violations": int(prev_viol),
        "contractor_compliance": int(contractor), "emergency_equipment_ok": int(emergency),
        "inspection_score": float(score), "production_tonnes": float(production),
    }

    errors = validate_inspection(data)
    if errors:
        for e in errors:
            st.error(e)
        return

    with st.spinner("Running CoalMineAI risk analysis..."):
        try:
            prediction, probability = predict_risk(data)  # 1) predict first, nothing written yet
        except Exception:
            log.exception("Prediction failed")
            st.error("The model could not score this inspection (e.g. an unrecognised location value). "
                     "Nothing was saved.")
            return
        try:
            inspection_id = save_inspection_with_prediction(data, prediction, probability)  # 2) atomic save
        except Exception:
            log.exception("Save failed")
            st.error("The inspection could not be saved to the database. Nothing was saved; please retry.")
            return

    st.success(f"Inspection #{inspection_id} successfully processed.")
    if normalize_risk(prediction) == "HIGH":
        st.warning("HIGH compliance risk detected. Escalate to the safety officer.")
    ai_panel(prediction, probability, f"Model: {MODEL_VERSION}")


PAGES = {
    "Dashboard": page_dashboard,
    "Inspector Data Entry": page_data_entry,
    "Inspections": lambda: table_page(
        "DATABASE INTELLIGENCE", "Inspection Records",
        f"""SELECT i.inspection_id, m.mine_name, i.inspection_date, i.inspection_time, i.location,
                   i.methane_percent, i.co_ppm, i.temperature_c, i.humidity_percent, i.worker_count,
                   i.attendance_percent, i.inspection_score, i.production_tonnes
            FROM inspections i JOIN mines m ON i.mine_id = m.mine_id
            ORDER BY i.inspection_id DESC LIMIT {TABLE_ROW_LIMIT}""",
        "No inspection records available."),
    "Predictions": lambda: table_page(
        "AI INTELLIGENCE", "Prediction History",
        f"""SELECT prediction_id, inspection_id, compliance_risk, prediction_probability,
                   model_version, predicted_at
            FROM predictions ORDER BY prediction_id DESC LIMIT {TABLE_ROW_LIMIT}""",
        "No prediction records available."),
    "Workers": lambda: table_page(
        "WORKFORCE INTELLIGENCE", "Worker Records",
        f"""SELECT worker_id, mine_id, worker_name, role, contractor, attendance_percent
            FROM workers ORDER BY worker_id LIMIT {TABLE_ROW_LIMIT}""",
        "No worker records available."),
    "Equipment": lambda: table_page(
        "ASSET INTELLIGENCE", "Equipment Records",
        f"""SELECT equipment_id, mine_id, equipment_type, condition, status
            FROM equipment ORDER BY equipment_id LIMIT {TABLE_ROW_LIMIT}""",
        "No equipment records available."),
}

try:
    PAGES[menu]()
except Exception:
    log.exception("Unhandled error on page %s", menu)
    st.error("Something went wrong loading this page. The error has been logged.")

st.markdown('<div class="footer">COALMINEAI · AI SAFETY & COMPLIANCE COMMAND CENTER · RANDOM FOREST ENGINE</div>',
            unsafe_allow_html=True)