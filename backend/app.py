from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)

# ==============================
# FILE PATH CONFIG
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

RAW_DATA_PATH = os.path.join(PROJECT_DIR, "dataset", "raw_data.csv")
CLEAN_DATA_PATH = os.path.join(PROJECT_DIR, "dataset", "clean_data.csv")
FINAL_DATA_PATH = os.path.join(PROJECT_DIR, "dataset", "final_traffic_data.csv")


# ==============================
# HELPER FUNCTIONS
# ==============================

def load_csv(file_path):
    if not os.path.exists(file_path):
        return None

    df = pd.read_csv(file_path)
    return df


def dataframe_to_json(df, limit=100):
    return df.head(limit).to_dict(orient="records")


# ==============================
# HOME ENDPOINT
# ==============================

@app.route("/")
def home():
    return jsonify({
        "project": "Smart Traffic Monitoring AI",
        "description": "API backend for traffic monitoring dataset, AI prediction, clustering, and anomaly detection.",
        "available_endpoints": [
            "/api/data/raw",
            "/api/data/clean",
            "/api/data/final",
            "/api/summary",
            "/api/prediction",
            "/api/anomaly",
            "/api/clustering",
            "/api/visualization"
        ]
    })


# ==============================
# DATA ENDPOINTS
# ==============================

@app.route("/api/data/raw")
def get_raw_data():
    df = load_csv(RAW_DATA_PATH)

    if df is None:
        return jsonify({"error": "raw_data.csv not found"}), 404

    return jsonify({
        "status": "success",
        "data_type": "raw_data",
        "total_rows": len(df),
        "columns": list(df.columns),
        "data": dataframe_to_json(df, limit=100)
    })


@app.route("/api/data/clean")
def get_clean_data():
    df = load_csv(CLEAN_DATA_PATH)

    if df is None:
        return jsonify({"error": "clean_data.csv not found"}), 404

    return jsonify({
        "status": "success",
        "data_type": "clean_data",
        "total_rows": len(df),
        "columns": list(df.columns),
        "data": dataframe_to_json(df, limit=100)
    })


@app.route("/api/data/final")
def get_final_data():
    df = load_csv(FINAL_DATA_PATH)

    if df is None:
        return jsonify({"error": "final_traffic_data.csv not found"}), 404

    return jsonify({
        "status": "success",
        "data_type": "final_traffic_data",
        "total_rows": len(df),
        "columns": list(df.columns),
        "data": dataframe_to_json(df, limit=100)
    })


# ==============================
# SUMMARY ENDPOINT
# ==============================

@app.route("/api/summary")
def get_summary():
    df = load_csv(FINAL_DATA_PATH)

    if df is None:
        return jsonify({"error": "final_traffic_data.csv not found"}), 404

    total_vehicles = int(df["vehicle_count"].sum())
    average_speed = round(float(df["average_speed"].mean()), 2)
    average_congestion = round(float(df["predicted_congestion"].mean()), 2)

    total_anomaly = int((df["anomaly_label"] == "Anomaly").sum())

    most_congested_road = (
        df.groupby("road_name")["predicted_congestion"]
        .mean()
        .sort_values(ascending=False)
        .idxmax()
    )

    return jsonify({
        "status": "success",
        "summary": {
            "total_vehicles": total_vehicles,
            "average_speed": average_speed,
            "average_predicted_congestion": average_congestion,
            "total_anomaly": total_anomaly,
            "most_congested_road": most_congested_road
        }
    })


# ==============================
# PREDICTION ENDPOINT
# ==============================

@app.route("/api/prediction")
def get_prediction_data():
    df = load_csv(FINAL_DATA_PATH)

    if df is None:
        return jsonify({"error": "final_traffic_data.csv not found"}), 404

    selected_columns = [
        "timestamp",
        "road_name",
        "vehicle_count",
        "average_speed",
        "traffic_density",
        "predicted_congestion",
        "predicted_congestion_level"
    ]

    return jsonify({
        "status": "success",
        "method": "Random Forest Regression",
        "target": "traffic_density",
        "output": "predicted_congestion",
        "data": dataframe_to_json(df[selected_columns], limit=100)
    })


# ==============================
# ANOMALY ENDPOINT
# ==============================

@app.route("/api/anomaly")
def get_anomaly_data():
    df = load_csv(FINAL_DATA_PATH)

    if df is None:
        return jsonify({"error": "final_traffic_data.csv not found"}), 404

    anomaly_df = df[df["anomaly_label"] == "Anomaly"]

    selected_columns = [
        "timestamp",
        "road_name",
        "vehicle_count",
        "average_speed",
        "road_occupancy",
        "traffic_density",
        "anomaly_label",
        "anomaly_score"
    ]

    return jsonify({
        "status": "success",
        "method": "Isolation Forest",
        "total_anomaly": int(len(anomaly_df)),
        "data": dataframe_to_json(anomaly_df[selected_columns], limit=100)
    })


# ==============================
# CLUSTERING ENDPOINT
# ==============================

@app.route("/api/clustering")
def get_clustering_data():
    df = load_csv(FINAL_DATA_PATH)

    if df is None:
        return jsonify({"error": "final_traffic_data.csv not found"}), 404

    selected_columns = [
        "road_name",
        "vehicle_count",
        "car_count",
        "motorcycle_count",
        "bus_count",
        "truck_count",
        "average_speed",
        "vehicle_cluster",
        "cluster_interpretation"
    ]

    cluster_summary = (
        df.groupby(["vehicle_cluster", "cluster_interpretation"])
        .size()
        .reset_index(name="total_records")
        .to_dict(orient="records")
    )

    return jsonify({
        "status": "success",
        "method": "K-Means Clustering",
        "cluster_summary": cluster_summary,
        "data": dataframe_to_json(df[selected_columns], limit=100)
    })


# ==============================
# VISUALIZATION ENDPOINT
# ==============================

@app.route("/api/visualization")
def get_visualization_data():
    df = load_csv(FINAL_DATA_PATH)

    if df is None:
        return jsonify({"error": "final_traffic_data.csv not found"}), 404

    vehicle_trend = (
        df.groupby("date")["vehicle_count"]
        .sum()
        .reset_index()
        .to_dict(orient="records")
    )

    vehicle_by_road = (
        df.groupby("road_name")[["car_count", "motorcycle_count", "bus_count", "truck_count"]]
        .sum()
        .reset_index()
        .to_dict(orient="records")
    )

    congestion_by_road = (
        df.groupby("road_name")["predicted_congestion"]
        .mean()
        .round(2)
        .reset_index()
        .to_dict(orient="records")
    )

    return jsonify({
        "status": "success",
        "visualization_data": {
            "vehicle_trend": vehicle_trend,
            "vehicle_by_road": vehicle_by_road,
            "congestion_by_road": congestion_by_road
        }
    })


# ==============================
# RUN APP
# ==============================

if __name__ == "__main__":
    app.run(debug=True)
    