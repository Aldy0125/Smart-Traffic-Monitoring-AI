import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

TOTAL_ROWS = 1000
OUTPUT_DIR = "../dataset"
OUTPUT_FILE = "raw_data.csv"

locations = [
    {
        "location_id": "LOC_001",
        "road_name": "Jl. Sisingamangaraja",
        "latitude": 2.3321,
        "longitude": 99.0654,
        "base_traffic": 95
    },
    {
        "location_id": "LOC_002",
        "road_name": "Jl. Sudirman",
        "latitude": 2.3348,
        "longitude": 99.0701,
        "base_traffic": 80
    },
    {
        "location_id": "LOC_003",
        "road_name": "Jl. Gatot Subroto",
        "latitude": 2.3375,
        "longitude": 99.0729,
        "base_traffic": 70
    },
    {
        "location_id": "LOC_004",
        "road_name": "Jl. Merdeka",
        "latitude": 2.3402,
        "longitude": 99.0752,
        "base_traffic": 60
    },
    {
        "location_id": "LOC_005",
        "road_name": "Jl. Ahmad Yani",
        "latitude": 2.3429,
        "longitude": 99.0788,
        "base_traffic": 85
    }
]

weather_options = ["Clear", "Cloudy", "Rainy", "Foggy"]


def get_time_factor(hour):
    if 6 <= hour <= 9:
        return 1.6
    elif 16 <= hour <= 19:
        return 1.8
    elif 11 <= hour <= 13:
        return 1.2
    elif 22 <= hour or hour <= 4:
        return 0.5
    else:
        return 1.0


def get_weather_factor(weather):
    if weather == "Clear":
        return 1.0
    elif weather == "Cloudy":
        return 1.05
    elif weather == "Rainy":
        return 1.25
    elif weather == "Foggy":
        return 1.15
    return 1.0


def calculate_speed(vehicle_count, weather):
    base_speed = 65 - (vehicle_count * 0.25)

    if weather == "Rainy":
        base_speed -= 8
    elif weather == "Foggy":
        base_speed -= 6
    elif weather == "Cloudy":
        base_speed -= 3

    speed = base_speed + np.random.normal(0, 4)
    return round(max(5, min(speed, 70)), 2)


def calculate_occupancy(vehicle_count):
    occupancy = (vehicle_count / 180) * 100
    occupancy += np.random.normal(0, 5)
    return round(max(5, min(occupancy, 100)), 2)


def split_vehicle_types(vehicle_count):
    motorcycle_ratio = np.random.uniform(0.50, 0.65)
    car_ratio = np.random.uniform(0.25, 0.35)
    bus_ratio = np.random.uniform(0.02, 0.06)

    motorcycle_count = int(vehicle_count * motorcycle_ratio)
    car_count = int(vehicle_count * car_ratio)
    bus_count = int(vehicle_count * bus_ratio)

    truck_count = vehicle_count - motorcycle_count - car_count - bus_count

    if truck_count < 0:
        truck_count = 0

    return car_count, motorcycle_count, bus_count, truck_count


def generate_dataset(total_rows):
    data = []
    start_time = datetime(2026, 5, 1, 0, 0, 0)

    for i in range(total_rows):
        current_time = start_time + timedelta(minutes=15 * i)
        hour = current_time.hour

        location = random.choice(locations)
        weather = random.choice(weather_options)

        time_factor = get_time_factor(hour)
        weather_factor = get_weather_factor(weather)

        vehicle_count = int(
            np.random.normal(
                location["base_traffic"] * time_factor * weather_factor,
                12
            )
        )

        vehicle_count = max(5, vehicle_count)

        car_count, motorcycle_count, bus_count, truck_count = split_vehicle_types(vehicle_count)
        average_speed = calculate_speed(vehicle_count, weather)
        road_occupancy = calculate_occupancy(vehicle_count)

        data.append({
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "location_id": location["location_id"],
            "road_name": location["road_name"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "vehicle_count": vehicle_count,
            "car_count": car_count,
            "motorcycle_count": motorcycle_count,
            "bus_count": bus_count,
            "truck_count": truck_count,
            "average_speed": average_speed,
            "road_occupancy": road_occupancy,
            "weather_condition": weather
        })

    return pd.DataFrame(data)


def add_missing_values(df):
    columns_with_missing = [
        "vehicle_count",
        "average_speed",
        "road_occupancy",
        "weather_condition"
    ]

    for col in columns_with_missing:
        missing_indices = df.sample(frac=0.03, random_state=random.randint(1, 100)).index
        df.loc[missing_indices, col] = np.nan

    return df


def add_outliers(df):
    outlier_indices = df.sample(frac=0.03, random_state=99).index

    for idx in outlier_indices:
        df.loc[idx, "vehicle_count"] = int(np.random.randint(220, 350))
        df.loc[idx, "average_speed"] = round(np.random.uniform(3, 12), 2)
        df.loc[idx, "road_occupancy"] = round(np.random.uniform(90, 100), 2)

        total_vehicle = int(df.loc[idx, "vehicle_count"])
        car_count, motorcycle_count, bus_count, truck_count = split_vehicle_types(total_vehicle)

        df.loc[idx, "car_count"] = car_count
        df.loc[idx, "motorcycle_count"] = motorcycle_count
        df.loc[idx, "bus_count"] = bus_count
        df.loc[idx, "truck_count"] = truck_count

    return df


def main():
    df = generate_dataset(TOTAL_ROWS)
    df = add_missing_values(df)
    df = add_outliers(df)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    df.to_csv(output_path, index=False)

    print("Raw traffic dataset berhasil dibuat.")
    print(f"File disimpan di: {output_path}")
    print(f"Jumlah baris: {len(df)}")
    print(f"Jumlah kolom: {len(df.columns)}")
    print("\nPreview data:")
    print(df.head())


if __name__ == "__main__":
    main()