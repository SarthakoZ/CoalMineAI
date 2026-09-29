import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


df = pd.read_csv("mineshield_synthetic_training_data.csv")


unnecessary_col = ["mine_id", "compliance_risk"]

X = df.drop(unnecessary_col, axis=1)
y = df["compliance_risk"]


categorical_col = [
    "location"
]

numerical_col = [
    "methane_percent",
    "co_ppm",
    "temperature_c",
    "humidity_percent",
    "worker_count",
    "attendance_percent",
    "helmet_compliance",
    "ppe_compliance",
    "equipment_condition",
    "safety_observation_level",
    "previous_violations",
    "contractor_compliance",
    "emergency_equipment_ok",
    "inspection_score",
    "production_tonnes"
]


numerical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])


categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])


preprocessor = ColumnTransformer([
    ("numerical", numerical_pipeline, numerical_col),
    ("categorical", categorical_pipeline, categorical_col)
])


model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)


pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


pipeline.fit(X_train, y_train)


y_pred = pipeline.predict(X_test)


accuracy = accuracy_score(y_test, y_pred)

print("Model Training Completed")
print("Accuracy:", round(accuracy * 100, 2), "%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))


joblib.dump(pipeline, "mineshield_compliance_model.pkl")

print("\nModel saved as mineshield_compliance_model.pkl")