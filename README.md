# Smart Traffic Monitoring AI

AI-Based Interactive Traffic Monitoring Dashboard for Congestion Prediction, Vehicle Pattern Clustering, and Anomaly Detection.

## 1. Project Overview

Smart Traffic Monitoring AI is an interactive visualization project developed for the Interactive Visualization Engineering course. This project simulates traffic monitoring data from CCTV or traffic sensors, processes the data using AI/ML models, and visualizes the results through an interactive Looker Studio dashboard.

The system is designed to analyze traffic volume, vehicle type distribution, average speed, road occupancy, congestion level, vehicle patterns, and traffic anomalies. Although this project uses a realistic dummy dataset, the system architecture can be extended into a real-time traffic monitoring system using CCTV, IoT sensors, traffic APIs, databases, or a Flask backend.

## 2. Main Objectives

The objectives of this project are:

1. Generate a realistic dummy traffic dataset that simulates CCTV or traffic sensor data.
2. Clean and preprocess raw traffic data into a structured dataset.
3. Apply AI/ML models for traffic congestion prediction, vehicle clustering, and anomaly detection.
4. Build an interactive dashboard using Looker Studio.
5. Provide a simple Flask API backend for accessing traffic data and AI/ML results.
6. Prepare the project for future development into a real-time smart traffic monitoring system.

## 3. Main Features

- Realistic dummy traffic dataset
- Raw and clean dataset
- AI-based congestion prediction
- Vehicle pattern clustering
- Traffic anomaly detection
- Interactive Looker Studio dashboard
- Traffic congestion map
- Summary scorecards
- Vehicle trend visualization
- Vehicle type comparison
- Average speed vs vehicle count scatter plot
- Alert and anomaly table
- Interactive filters by date, road name, and weather condition
- Flask API backend

## 4. AI/ML Methods

This project uses three main AI/ML methods:

| Task | Method | Output |
|---|---|---|
| Traffic congestion prediction | Random Forest Regression | predicted_congestion |
| Vehicle pattern clustering | K-Means Clustering | vehicle_cluster |
| Traffic anomaly detection | Isolation Forest | anomaly_label |
| Congestion level classification | Rule-based classification | congestion_level |

## 5. Dataset Description

The project uses three CSV datasets:

| File | Description |
|---|---|
| `raw_data.csv` | Raw simulated traffic data with missing values, noise, and outliers |
| `clean_data.csv` | Cleaned dataset after preprocessing |
| `final_traffic_data.csv` | Final dataset with AI/ML outputs |

Main dataset fields:

| Field | Description |
|---|---|
| timestamp | Traffic data recording time |
| date | Date extracted from timestamp |
| hour | Hour extracted from timestamp |
| day_name | Day name |
| location_id | Monitoring location ID |
| road_name | Road name |
| latitude | Latitude coordinate |
| longitude | Longitude coordinate |
| vehicle_count | Total detected vehicles |
| car_count | Number of cars |
| motorcycle_count | Number of motorcycles |
| bus_count | Number of buses |
| truck_count | Number of trucks |
| average_speed | Average vehicle speed |
| road_occupancy | Road occupancy percentage |
| weather_condition | Weather condition |
| traffic_density | Calculated traffic density |
| congestion_level | Rule-based congestion category |
| predicted_congestion | AI-predicted congestion value |
| predicted_congestion_level | Predicted congestion category |
| vehicle_cluster | Vehicle pattern cluster |
| cluster_interpretation | Interpretation of cluster result |
| anomaly_label | Normal or anomaly label |
| anomaly_score | Anomaly score from Isolation Forest |

## 6. Project Structure

```text
Smart-Traffic-Monitoring-AI/
│
├── dataset/
│   ├── raw_data.csv
│   ├── clean_data.csv
│   └── final_traffic_data.csv
│
├── data_pipeline/
│   ├── generate_dummy_traffic_data.py
│   └── preprocessing.py
│
├── ai_model/
│   ├── train_model.py
│   ├── prediction_model.pkl
│   ├── clustering_model.pkl
│   ├── anomaly_model.pkl
│   ├── scaler.pkl
│   └── model_summary.txt
│
├── dashboard/
│   ├── looker_dashboard_link.txt
│   └── dashboard_documentation.md
│
├── backend/
│   ├── app.py
│   └── requirements.txt
│
├── paper/
├── presentation/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 7. Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Flask
- Looker Studio
- Google Sheets
- Git
- GitHub

## 8. How to Run the Project

### 8.1 Clone Repository

```bash
git clone https://github.com/Aldy0125/Smart-Traffic-Monitoring-AI.git
cd Smart-Traffic-Monitoring-AI
```

### 8.2 Create Virtual Environment

```bash
python -m venv venv
```

### 8.3 Activate Virtual Environment

For Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

### 8.4 Install Dependencies

```bash
pip install -r requirements.txt
```

## 9. Generate Dataset

Go to the data pipeline folder:

```bash
cd data_pipeline
```

Run the dataset generator:

```bash
python generate_dummy_traffic_data.py
```

Output:

```text
dataset/raw_data.csv
```

## 10. Run Data Preprocessing

Still inside the `data_pipeline` folder, run:

```bash
python preprocessing.py
```

Output:

```text
dataset/clean_data.csv
```

## 11. Train AI/ML Models

Go to the AI model folder:

```bash
cd ../ai_model
```

Run the model training script:

```bash
python train_model.py
```

Outputs:

```text
dataset/final_traffic_data.csv

ai_model/prediction_model.pkl
ai_model/clustering_model.pkl
ai_model/anomaly_model.pkl
ai_model/scaler.pkl
ai_model/model_summary.txt
```

## 12. Model Evaluation Result

The AI/ML training process produced the following results:

| Model | Metric | Result |
|---|---|---|
| Random Forest Regression | MAE | 1.08 |
| Random Forest Regression | RMSE | 2.46 |
| Random Forest Regression | R2 Score | 1.00 |
| K-Means Clustering | Silhouette Score | 0.38 |
| Isolation Forest | Anomaly Count | 50 |
| Isolation Forest | Anomaly Percentage | 5.00% |

## 13. Run Flask API Backend

Go to the backend folder:

```bash
cd ../backend
```

Run the Flask application:

```bash
python app.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

## 14. API Endpoints

| Endpoint | Description |
|---|---|
| `/` | Home endpoint and API information |
| `/api/data/raw` | Get raw traffic dataset |
| `/api/data/clean` | Get clean traffic dataset |
| `/api/data/final` | Get final dataset with AI/ML results |
| `/api/summary` | Get traffic summary |
| `/api/prediction` | Get congestion prediction results |
| `/api/anomaly` | Get anomaly detection results |
| `/api/clustering` | Get vehicle clustering results |
| `/api/visualization` | Get summarized data for visualization |

Example summary endpoint:

```text
http://127.0.0.1:5000/api/summary
```

Example response:

```json
{
  "status": "success",
  "summary": {
    "average_predicted_congestion": 69.24,
    "average_speed": 35.67,
    "most_congested_road": "Jl. Sisingamangaraja",
    "total_anomaly": 50,
    "total_vehicles": 102112
  }
}
```

## 15. Dashboard

The dashboard was built using Looker Studio and connected to Google Sheets.

Dashboard components:

1. Total Vehicles scorecard
2. Average Speed scorecard
3. Average Congestion scorecard
4. Total Anomaly scorecard
5. Traffic Volume Trend line chart
6. Vehicle Type by Road bar chart
7. Traffic Proportion by Road donut chart
8. Average Speed vs Vehicle Count scatter plot
9. Congestion map
10. Alert and anomaly table
11. Date range filter
12. Road name filter
13. Weather condition filter

The dashboard link is stored in:

```text
dashboard/looker_dashboard_link.txt
```

Dashboard documentation is available in:

```text
dashboard/dashboard_documentation.md
```

## 16. Dashboard Link

Looker Studio Dashboard:

```text
https://datastudio.google.com/u/0/reporting/82e0164a-5bed-4bd9-a4ab-ec3016332d6b/page/e1nxF/edit
```

## 17. Project Workflow

```text
Python Data Generator
        ↓
raw_data.csv
        ↓
Data Preprocessing
        ↓
clean_data.csv
        ↓
AI/ML Model Training
        ↓
final_traffic_data.csv
        ↓
Google Sheets
        ↓
Looker Studio Dashboard
        ↓
Traffic Insight and Visualization
```

Optional backend workflow:

```text
final_traffic_data.csv
        ↓
Flask API
        ↓
JSON Endpoint
        ↓
Data Access / Future Integration
```

## 18. Important Notes

This project uses a realistic dummy dataset, not real-time CCTV data. The data was generated using Python to simulate traffic conditions from CCTV or traffic sensors.

However, the system is designed so it can be extended into a real-time monitoring system in the future using:

- CCTV data
- IoT traffic sensors
- Public traffic APIs
- Real-time database
- Flask API integration
- Automatic data refresh pipeline

## 19. Future Development

Possible future improvements:

1. Integrate real CCTV or IoT sensor data.
2. Store traffic data in a real database such as MySQL, PostgreSQL, or Firebase.
3. Add real-time data update using API or scheduled pipeline.
4. Improve AI model with larger and real-world traffic datasets.
5. Add map-based congestion alert with automatic notification.
6. Deploy Flask API to cloud hosting.
7. Build a custom web dashboard using React or Flask frontend.

## 20. Author

**Aldy Putra Manurung**  
Electrical Engineering Student  
Institut Teknologi Del

## 21. Project Status

```text
Dataset generation      : Completed
Data preprocessing      : Completed
AI/ML model training    : Completed
Looker Studio dashboard : Completed
Flask API backend       : Completed
GitHub documentation    : Completed
```