# Smart Traffic Monitoring AI Dashboard Documentation

## 1. Dashboard Overview

This dashboard is part of the **Smart Traffic Monitoring AI** project. The dashboard is designed to visualize simulated traffic monitoring data and AI/ML analysis results, including traffic congestion prediction, vehicle pattern clustering, and anomaly detection.

The dashboard was built using **Looker Studio** and connected to **Google Sheets** as the data source. The dataset used in this dashboard is `final_traffic_data.csv`, which contains cleaned traffic data and AI/ML output generated from the Python data pipeline.

This dashboard helps users monitor traffic conditions, identify congested roads, detect anomaly patterns, and understand traffic distribution through interactive visualizations.

---

## 2. Data Source

The dashboard uses the final dataset:

```text
dataset/final_traffic_data.csv
```

The dataset was generated through the following pipeline:

```text
raw_data.csv
→ preprocessing.py
→ clean_data.csv
→ train_model.py
→ final_traffic_data.csv
→ Google Sheets
→ Looker Studio Dashboard
```

The dataset contains simulated traffic data from CCTV or traffic sensor scenarios. The data is not real-time CCTV data, but it is designed to resemble real traffic data with time-series patterns, multivariable features, outliers, missing values, and traffic variations.

Main dataset fields:

| Field | Description |
|---|---|
| timestamp | Traffic data recording time |
| date | Date extracted from timestamp |
| hour | Hour extracted from timestamp |
| day_name | Day name extracted from timestamp |
| location_id | Traffic monitoring location ID |
| road_name | Road name |
| latitude | Road latitude coordinate |
| longitude | Road longitude coordinate |
| vehicle_count | Total detected vehicles |
| car_count | Number of cars |
| motorcycle_count | Number of motorcycles |
| bus_count | Number of buses |
| truck_count | Number of trucks |
| average_speed | Average vehicle speed |
| road_occupancy | Road occupancy percentage |
| weather_condition | Weather condition |
| traffic_density | Calculated traffic density |
| congestion_level | Rule-based congestion level |
| predicted_congestion | Predicted congestion value |
| predicted_congestion_level | Predicted congestion category |
| vehicle_cluster | Vehicle pattern cluster |
| cluster_interpretation | Cluster interpretation |
| anomaly_label | Normal or anomaly traffic label |
| anomaly_score | Isolation Forest anomaly score |

---

## 3. AI/ML Output Used in Dashboard

The dashboard uses several AI/ML output fields generated from the model training process.

| AI/ML Task | Method | Output Field |
|---|---|---|
| Traffic congestion prediction | Random Forest Regression | predicted_congestion |
| Vehicle pattern clustering | K-Means Clustering | vehicle_cluster, cluster_interpretation |
| Traffic anomaly detection | Isolation Forest | anomaly_label, anomaly_score |
| Congestion classification | Rule-based classification | congestion_level |

Additional calculated fields were also created in Looker Studio to support dashboard visualization:

| Calculated Field | Function |
|---|---|
| predicted_congestion_num | Converts predicted congestion into numeric format |
| anomaly_count | Counts anomaly records |
| geo_location_fixed | Provides fixed location coordinates for map visualization |

---

## 4. Dashboard Components

The dashboard consists of several main visualization components.

---

### 4.1 Summary Scorecards

The summary scorecards provide quick information about the overall traffic condition.

Scorecards used:

1. **Total Vehicles**
2. **Average Speed**
3. **Average Congestion**
4. **Total Anomaly**

Field configuration:

```text
Total Vehicles:
Metric: SUM vehicle_count

Average Speed:
Metric: AVG average_speed

Average Congestion:
Metric: AVG predicted_congestion_num

Total Anomaly:
Metric: SUM anomaly_count
```

These scorecards allow users to quickly understand total traffic volume, average speed, congestion level, and anomaly frequency.

---

### 4.2 Traffic Volume Trend

The line chart shows the trend of total vehicle count over time.

Field configuration:

```text
Chart type: Time Series Chart
Dimension: date
Metric: SUM vehicle_count
```

Purpose:

This chart helps identify traffic volume changes across different dates. It can be used to observe increasing or decreasing traffic trends.

---

### 4.3 Vehicle Type by Road

The bar chart compares the number of vehicles by type for each road.

Field configuration:

```text
Chart type: Bar Chart
Dimension: road_name
Metrics:
- SUM car_count
- SUM motorcycle_count
- SUM bus_count
- SUM truck_count
```

Purpose:

This chart helps users understand the composition of vehicle types on each road. For example, some roads may be dominated by motorcycles, while others may have more cars or heavy vehicles.

---

### 4.4 Traffic Proportion by Road

The donut chart shows the proportion of total traffic volume for each road.

Field configuration:

```text
Chart type: Donut Chart
Dimension: road_name
Metric: SUM vehicle_count
```

Purpose:

This chart helps compare the traffic contribution of each road to the overall vehicle count.

---

### 4.5 Average Speed vs Vehicle Count

The scatter plot shows the relationship between traffic volume and average speed.

Field configuration:

```text
Chart type: Scatter Plot
Dimension: road_name
X-axis: SUM vehicle_count
Y-axis: AVG average_speed
```

Purpose:

This chart helps show the relationship between the number of vehicles and average speed. In general, roads with higher vehicle counts tend to have lower average speeds, indicating possible congestion.

---

### 4.6 Congestion Map

The map visualizes road locations and traffic congestion conditions.

Field configuration:

```text
Chart type: Google Maps Bubble Map
Location: geo_location_fixed
Tooltip: road_name
Size: SUM vehicle_count
Color metric: AVG predicted_congestion_num
```

Purpose:

The map helps users identify traffic conditions by road location. Bubble size represents the total number of vehicles, while color represents the predicted congestion level.

---

### 4.7 Alert and Anomaly Table

The alert table displays traffic congestion and anomaly information.

Fields used:

```text
road_name
congestion_level
anomaly_label
vehicle_count
average_speed
predicted_congestion_num
anomaly_count
```

Purpose:

This table helps identify roads with abnormal traffic conditions, high congestion levels, or detected anomalies.

---

## 5. Dashboard Filters

The dashboard includes interactive filters to support data exploration.

Filters used:

1. **Date Range Filter**
2. **Road Name Filter**
3. **Weather Condition Filter**

Filter configuration:

```text
Date Range Filter:
Field: date

Road Name Filter:
Field: road_name

Weather Condition Filter:
Field: weather_condition
```

Purpose:

These filters allow users to analyze traffic conditions based on specific dates, road locations, and weather conditions.

---

## 6. Calculated Fields

Several calculated fields were created in Looker Studio to support dashboard visualization.

---

### 6.1 predicted_congestion_num

This field converts `predicted_congestion` into numeric format so it can be used for scorecards, maps, and charts.

Formula:

```sql
CAST(predicted_congestion AS NUMBER)
```

---

### 6.2 anomaly_count

This field converts anomaly labels into numeric values so the total anomaly can be counted.

Formula:

```sql
CASE
  WHEN anomaly_label = "Anomaly" THEN 1
  ELSE 0
END
```

---

### 6.3 geo_location_fixed

This field provides fixed latitude and longitude values based on the road name. It is used for map visualization.

Formula:

```sql
CASE
  WHEN road_name = "Jl. Sisingamangaraja" THEN "2.3321,99.0654"
  WHEN road_name = "Jl. Sudirman" THEN "2.3348,99.0701"
  WHEN road_name = "Jl. Gatot Subroto" THEN "2.3375,99.0729"
  WHEN road_name = "Jl. Merdeka" THEN "2.3402,99.0752"
  WHEN road_name = "Jl. Ahmad Yani" THEN "2.3429,99.0788"
  ELSE "2.3348,99.0701"
END
```

The data type for this field was set as:

```text
Geo → Latitude, Longitude
```

---

## 7. Dashboard Link

The Looker Studio dashboard link is stored in:

```text
dashboard/looker_dashboard_link.txt
```

Dashboard link:

```text
https://datastudio.google.com/u/0/reporting/82e0164a-5bed-4bd9-a4ab-ec3016332d6b/page/e1nxF/edit
```

---

## 8. Dashboard Interpretation

The dashboard can be interpreted as follows:

1. **Total Vehicles** shows the total number of vehicles detected in the simulated traffic dataset.
2. **Average Speed** shows the average speed of vehicles across all monitored roads.
3. **Average Congestion** shows the average predicted congestion value generated by the AI model.
4. **Total Anomaly** shows the total number of traffic anomaly records detected by the anomaly detection model.
5. **Traffic Volume Trend** shows how traffic volume changes over time.
6. **Vehicle Type by Road** shows the distribution of cars, motorcycles, buses, and trucks for each road.
7. **Traffic Proportion by Road** shows which road contributes the most traffic volume.
8. **Average Speed vs Vehicle Count** shows the relationship between vehicle volume and speed.
9. **Congestion Map** shows traffic conditions based on road location.
10. **Alert and Anomaly Table** highlights roads with congestion and anomaly information.

---

## 9. Notes

This dashboard uses a realistic dummy traffic dataset, not real-time CCTV data. However, the system architecture is designed so it can be developed into a real-time monitoring system in the future.

Possible future development:

1. Integration with real CCTV data.
2. Integration with IoT traffic sensors.
3. Real-time database connection.
4. Flask API backend for live data access.
5. Automatic dashboard refresh using Google Sheets or database integration.
6. More advanced AI models for congestion prediction.

---

## 10. Conclusion

The Smart Traffic Monitoring AI Dashboard successfully visualizes simulated traffic monitoring data and AI/ML results. The dashboard provides traffic trend analysis, vehicle type distribution, congestion mapping, anomaly detection, and interactive filtering.

This dashboard supports the main objective of the project, which is to develop an AI-based interactive visualization system for smart traffic monitoring. Although the current version uses simulated data, the system is structured so it can be extended into a real-time traffic monitoring system in the future.