import pandas as pd
import numpy as np
import os

INPUT_FILE = "../dataset/raw_data.csv"
OUTPUT_FILE = "../dataset/clean_data.csv"


def classify_congestion(row):
    speed = row["average_speed"]
    occupancy = row["road_occupancy"]

    if speed >= 45 and occupancy < 40:
        return "Low"
    elif speed >= 30 and occupancy < 65:
        return "Medium"
    elif speed >= 15 and occupancy < 85:
        return "High"
    else:
        return "Severe"


def detect_rule_based_anomaly(row):
    if row["vehicle_count"] > 220:
        return "Anomaly"
    elif row["average_speed"] < 10 and row["road_occupancy"] > 85:
        return "Anomaly"
    elif row["road_occupancy"] > 95:
        return "Anomaly"
    else:
        return "Normal"


def clean_numeric_column(df, column):
    df[column] = pd.to_numeric(df[column], errors="coerce")
    median_value = df[column].median()
    df[column] = df[column].fillna(median_value)
    return df


def cap_outlier(df, column, lower_limit=None, upper_limit=None):
    if lower_limit is not None:
        df[column] = np.where(df[column] < lower_limit, lower_limit, df[column])

    if upper_limit is not None:
        df[column] = np.where(df[column] > upper_limit, upper_limit, df[column])

    return df


def preprocess_data():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"File tidak ditemukan: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)

    print("Raw data berhasil dibaca.")
    print(f"Jumlah data awal: {df.shape[0]} baris")
    print(f"Jumlah kolom awal: {df.shape[1]} kolom")

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["timestamp"] = df["timestamp"].ffill()

    numeric_columns = [
        "vehicle_count",
        "car_count",
        "motorcycle_count",
        "bus_count",
        "truck_count",
        "average_speed",
        "road_occupancy",
        "latitude",
        "longitude"
    ]

    for col in numeric_columns:
        df = clean_numeric_column(df, col)

    df["weather_condition"] = df["weather_condition"].fillna("Unknown")
    df["weather_condition"] = df["weather_condition"].replace(
        "Unknown",
        df["weather_condition"].mode()[0]
    )

    df["location_id"] = df["location_id"].fillna("UNKNOWN_LOC")
    df["road_name"] = df["road_name"].fillna("Unknown Road")

    df = cap_outlier(df, "vehicle_count", lower_limit=0, upper_limit=300)
    df = cap_outlier(df, "average_speed", lower_limit=0, upper_limit=80)
    df = cap_outlier(df, "road_occupancy", lower_limit=0, upper_limit=100)

    vehicle_type_columns = [
        "car_count",
        "motorcycle_count",
        "bus_count",
        "truck_count"
    ]

    for col in vehicle_type_columns:
        df[col] = df[col].round().astype(int)
        df[col] = df[col].clip(lower=0)

    df["vehicle_count"] = (
        df["car_count"]
        + df["motorcycle_count"]
        + df["bus_count"]
        + df["truck_count"]
    )

    df["average_speed"] = df["average_speed"].round(2)
    df["road_occupancy"] = df["road_occupancy"].round(2)

    df["traffic_density"] = (
        df["vehicle_count"] * df["road_occupancy"] / 100
    ).round(2)

    df["congestion_level"] = df.apply(classify_congestion, axis=1)
    df["anomaly_label"] = df.apply(detect_rule_based_anomaly, axis=1)

    df["vehicle_cluster"] = -1
    df["predicted_congestion"] = df["traffic_density"]

    df["date"] = df["timestamp"].dt.date
    df["hour"] = df["timestamp"].dt.hour
    df["day_name"] = df["timestamp"].dt.day_name()

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
        "vehicle_cluster",
        "anomaly_label",
        "predicted_congestion"
    ]

    df = df[final_columns]

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nPreprocessing selesai.")
    print(f"File clean data disimpan di: {OUTPUT_FILE}")
    print(f"Jumlah data akhir: {df.shape[0]} baris")
    print(f"Jumlah kolom akhir: {df.shape[1]} kolom")
    print("\nMissing value setelah preprocessing:")
    print(df.isnull().sum())
    print("\nPreview clean data:")
    print(df.head())


if __name__ == "__main__":
    preprocess_data()