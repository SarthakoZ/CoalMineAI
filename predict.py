import pandas as pd
import joblib

from database import get_connection


MODEL_PATH = "model/mineshield_compliance_model.pkl"


model = joblib.load(MODEL_PATH)


def predict_inspection(inspection_id):

    connection = get_connection()
    cursor = connection.cursor()

    select_query = """
        SELECT
            location,
            methane_percent,
            co_ppm,
            temperature_c,
            humidity_percent,
            worker_count,
            attendance_percent,
            helmet_compliance,
            ppe_compliance,
            equipment_condition,
            safety_observation_level,
            previous_violations,
            contractor_compliance,
            emergency_equipment_ok,
            inspection_score,
            production_tonnes
        FROM inspections
        WHERE inspection_id = %s
    """

    cursor.execute(
        select_query,
        (inspection_id,)
    )

    result = cursor.fetchone()

    if result is None:
        print("Inspection not found.")
        cursor.close()
        connection.close()
        return

    columns = [
        "location",
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

    df = pd.DataFrame(
        [result],
        columns=columns
    )

    prediction = str(
        model.predict(df)[0]
    )

    probability = float(
        model.predict_proba(df).max()
    )

    model_version = "Random Forest v1"

    insert_query = """
        INSERT INTO predictions
        (
            inspection_id,
            compliance_risk,
            prediction_probability,
            model_version
        )
        VALUES
        (%s, %s, %s, %s)
    """

    cursor.execute(
        insert_query,
        (
            int(inspection_id),
            prediction,
            probability,
            model_version
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    print()
    print("Prediction completed successfully.")
    print("Inspection ID:", inspection_id)
    print("Compliance Risk:", prediction)
    print(
        "Probability:",
        round(probability * 100, 2),
        "%"
    )
    print("Model:", model_version)


if __name__ == "__main__":

    inspection_id = int(
        input("Enter inspection ID: ")
    )

    predict_inspection(
        inspection_id
    )