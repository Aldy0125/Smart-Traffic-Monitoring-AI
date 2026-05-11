import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, silhouette_score


INPUT_FILE = "../dataset/clean_data.csv"
OUTPUT_FILE = "../dataset/final_traffic_data.csv"

PREDICTION_MODEL_FILE = "prediction_model.pkl"
CLUSTERING_MODEL_FILE = "clustering_model.pkl"
ANOMALY_MODEL_FILE = "anomaly_model.pkl"
SCALER_FILE = "scaler.pkl"


def classify_congestion_from_prediction(value):
    if value < 35:
        return "Low"
    elif value < 70:
        return "Medium"
    elif value < 110:
        return "High"
    else:
        return "Severe"


def interpret_cluster(row):
    vehicle_count = row["vehicle_count"]
    average_speed = row["average_speed"]
    truck_count = row["truck_count"]
    bus_count = row["bus_count"]
    motorcycle_count = row["motorcycle_count"]
    car_count = row["car_count"]

    if vehicle_count < 70 and average_speed > 40:
        return "Light Traffic"
    elif motorcycle_count > car_count and vehicle_count >= 70:
        return "Motorcycle-Dominant Traffic"
    elif vehicle_count >= 120 and average_speed < 30:
        return "Heavy Congested Traffic"
    elif truck_count + bus_count > 20:
        return "Heavy Vehicle Traffic"
    else:
        return "Mixed Traffic"


def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def load_data():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"File tidak ditemukan: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)

    print_section("DATA LOADED")
    print(f"Jumlah baris: {df.shape[0]}")
    print(f"Jumlah kolom: {df.shape[1]}")
    print(df.head())

    return df


def prepare_data(df):
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    label_encoder = LabelEncoder()
    df["weather_encoded"] = label_encoder.fit_transform(df["weather_condition"])

    if "hour" not in df.columns:
        df["hour"] = df["timestamp"].dt.hour

    return df


def train_prediction_model(df):
    print_section("TRAINING RANDOM FOREST REGRESSION MODEL")

    feature_columns = [
        "vehicle_count",
        "car_count",
        "motorcycle_count",
        "bus_count",
        "truck_count",
        "average_speed",
        "road_occupancy",
        "hour",
        "weather_encoded"
    ]

    target_column = "traffic_density"

    X = df[feature_columns]
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        max_depth=10
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print("Evaluasi Model Prediksi Kemacetan:")
    print(f"MAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R2   : {r2:.2f}")

    df["predicted_congestion"] = model.predict(X).round(2)
    df["predicted_congestion_level"] = df["predicted_congestion"].apply(
        classify_congestion_from_prediction
    )

    joblib.dump(model, PREDICTION_MODEL_FILE)

    print(f"\nModel prediksi disimpan sebagai: {PREDICTION_MODEL_FILE}")

    return df, {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }


def train_clustering_model(df):
    print_section("TRAINING K-MEANS CLUSTERING MODEL")

    clustering_features = [
        "car_count",
        "motorcycle_count",
        "bus_count",
        "truck_count",
        "vehicle_count",
        "average_speed"
    ]

    X_cluster = df[clustering_features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_cluster)

    kmeans = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    cluster_labels = kmeans.fit_predict(X_scaled)
    df["vehicle_cluster"] = cluster_labels

    silhouette = silhouette_score(X_scaled, cluster_labels)

    print("Evaluasi K-Means Clustering:")
    print(f"Silhouette Score: {silhouette:.2f}")

    df["cluster_interpretation"] = df.apply(interpret_cluster, axis=1)

    joblib.dump(kmeans, CLUSTERING_MODEL_FILE)
    joblib.dump(scaler, SCALER_FILE)

    print(f"\nModel clustering disimpan sebagai: {CLUSTERING_MODEL_FILE}")
    print(f"Scaler disimpan sebagai: {SCALER_FILE}")

    print("\nJumlah data per cluster:")
    print(df["vehicle_cluster"].value_counts().sort_index())

    return df, {
        "Silhouette Score": silhouette
    }


def train_anomaly_model(df):
    print_section("TRAINING ISOLATION FOREST ANOMALY DETECTION MODEL")

    anomaly_features = [
        "vehicle_count",
        "average_speed",
        "road_occupancy",
        "traffic_density"
    ]

    X_anomaly = df[anomaly_features]

    anomaly_model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )

    anomaly_result = anomaly_model.fit_predict(X_anomaly)

    df["anomaly_score"] = anomaly_model.decision_function(X_anomaly).round(4)
    df["anomaly_label"] = np.where(
        anomaly_result == -1,
        "Anomaly",
        "Normal"
    )

    joblib.dump(anomaly_model, ANOMALY_MODEL_FILE)

    print(f"Model anomaly detection disimpan sebagai: {ANOMALY_MODEL_FILE}")

    print("\nJumlah data Normal dan Anomaly:")
    print(df["anomaly_label"].value_counts())

    anomaly_count = df[df["anomaly_label"] == "Anomaly"].shape[0]
    anomaly_percentage = (anomaly_count / df.shape[0]) * 100

    print(f"\nPersentase anomaly: {anomaly_percentage:.2f}%")

    return df, {
        "Anomaly Count": anomaly_count,
        "Anomaly Percentage": anomaly_percentage
    }


def save_final_dataset(df):
    print_section("SAVING FINAL DATASET")

    final_columns = [
        "timestamp",
        "date",
        "hour",
        "day_name",
        "location_id",
        "road_name",
        "latitude",
        "longitude",
        "vehicle_count",
        "car_count",
        "motorcycle_count",
        "bus_count",
        "truck_count",
        "average_speed",
        "road_occupancy",
        "weather_condition",
        "traffic_density",
        "congestion_level",
        "predicted_congestion",
        "predicted_congestion_level",
        "vehicle_cluster",
        "cluster_interpretation",
        "anomaly_label",
        "anomaly_score"
    ]

    df_final = df[final_columns]
    df_final.to_csv(OUTPUT_FILE, index=False)

    print(f"Final dataset berhasil disimpan ke: {OUTPUT_FILE}")
    print(f"Jumlah baris final: {df_final.shape[0]}")
    print(f"Jumlah kolom final: {df_final.shape[1]}")
    print(df_final.head())

    return df_final


def save_model_summary(prediction_metrics, clustering_metrics, anomaly_metrics):
    summary_text = f"""
SMART TRAFFIC MONITORING AI - MODEL SUMMARY

1. Traffic Congestion Prediction
Method: Random Forest Regression
Target: traffic_density
MAE: {prediction_metrics['MAE']:.2f}
RMSE: {prediction_metrics['RMSE']:.2f}
R2 Score: {prediction_metrics['R2']:.2f}

2. Vehicle Pattern Clustering
Method: K-Means Clustering
Number of Clusters: 4
Silhouette Score: {clustering_metrics['Silhouette Score']:.2f}

3. Traffic Anomaly Detection
Method: Isolation Forest
Anomaly Count: {anomaly_metrics['Anomaly Count']}
Anomaly Percentage: {anomaly_metrics['Anomaly Percentage']:.2f}%

Output Files:
- prediction_model.pkl
- clustering_model.pkl
- anomaly_model.pkl
- scaler.pkl
- final_traffic_data.csv
"""

    with open("model_summary.txt", "w", encoding="utf-8") as file:
        file.write(summary_text)

    print(summary_text)
    print("Model summary disimpan sebagai: model_summary.txt")


def main():
    df = load_data()
    df = prepare_data(df)

    df, prediction_metrics = train_prediction_model(df)
    df, clustering_metrics = train_clustering_model(df)
    df, anomaly_metrics = train_anomaly_model(df)

    save_final_dataset(df)

    save_model_summary(
        prediction_metrics,
        clustering_metrics,
        anomaly_metrics
    )

    print_section("TRAINING PROCESS FINISHED")
    print("Semua model AI/ML berhasil dibuat.")
    print("Dataset final sudah siap digunakan untuk Looker Studio atau Power BI.")


if __name__ == "__main__":
    main()