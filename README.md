# Smart Traffic Monitoring AI

AI-Based Interactive Traffic Monitoring Dashboard for Congestion Prediction, Vehicle Pattern Clustering, and Anomaly Detection.

## Description

This project is developed for the Interactive Visualization Engineering course. The system simulates realistic traffic data from CCTV or traffic sensors, processes the data using AI/ML models, and visualizes the results in an interactive dashboard.

The project uses a realistic dummy dataset, not real-time CCTV data. However, the system architecture is designed so it can be developed into a real-time system in the future using CCTV, IoT sensors, APIs, or databases.

## Main Features

- Realistic dummy traffic dataset
- Raw and clean dataset
- Traffic congestion prediction
- Vehicle pattern clustering
- Traffic anomaly detection
- Interactive dashboard using Looker Studio or Power BI
- Optional Flask API backend

## AI/ML Methods

1. Random Forest Regression for traffic congestion prediction
2. K-Means Clustering for vehicle pattern clustering
3. Isolation Forest for traffic anomaly detection
4. Rule-based classification for congestion level

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Flask
- Looker Studio
- Google Sheets
- GitHub

## Project Structure

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
├── backend/
├── paper/
├── presentation/
├── requirements.txt
└── README.md
```

## How to Run

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

```bash
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate Raw Dataset

```bash
cd data_pipeline
python generate_dummy_traffic_data.py
```

### 5. Run Data Preprocessing

```bash
python preprocessing.py
```

### 6. Train AI/ML Models

```bash
cd ../ai_model
python train_model.py
```

## Output Files

```text
dataset/raw_data.csv
dataset/clean_data.csv
dataset/final_traffic_data.csv

ai_model/prediction_model.pkl
ai_model/clustering_model.pkl
ai_model/anomaly_model.pkl
ai_model/scaler.pkl
ai_model/model_summary.txt
```

## Dashboard

The final dataset can be uploaded to Google Sheets and connected to Looker Studio.

Main dashboard components:

- Congestion map
- Summary scorecards
- Vehicle trend chart
- Vehicle type chart
- Scatter plot
- Actual vs predicted congestion chart
- Anomaly alert table
- Cluster distribution chart
- Detailed traffic table

## Project Status

Dataset generation, data preprocessing, and AI/ML model training have been completed. The next step is dashboard development using Looker Studio or Power BI.

## Author

Aldy Putra Manurung