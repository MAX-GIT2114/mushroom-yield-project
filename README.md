# Mushroom Yield Prediction Project

## Overview

This project focuses on building a data pipeline and machine learning workflow for predicting mushroom yield using polyhouse sensor data. The dataset contains environmental measurements such as temperature, humidity, and CO₂ concentration collected from cultivation units.

The project is structured to support data ingestion, validation, preprocessing, model training, and deployment-ready model storage.

---

## Project Structure

```text
mushroom-yield-project/
│
├── data/
│   ├── processed/        # Standardized datasets ready for modeling
│   └── raw/              # Raw sensor data uploads (excluded from Git)
│
├── models/               # Serialized production-ready model files
│
├── notebooks/            # Jupyter notebooks for exploratory analysis
│
├── src/
│   └── smoke_test.py     # Base validation environment script
│
├── .gitignore            # Excludes virtual environments and large data files
├── README.md             # Project documentation and workflow guide
└── requirements.txt      # Project dependencies
```

---

## Features

* CSV-based sensor data ingestion
* Data validation and quality checks
* Data preprocessing pipeline
* Exploratory Data Analysis (EDA)
* Machine Learning model training
* Mushroom yield prediction
* Model serialization and storage

---

## Dataset Fields

| Column        | Description                        |
| ------------- | ---------------------------------- |
| timestamp     | Sensor reading timestamp           |
| temperature_c | Temperature in Celsius             |
| humidity_pct  | Relative humidity (%)              |
| co2_ppm       | Carbon dioxide concentration (ppm) |
| yield_kg      | Mushroom yield (kg)                |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/MAX-GIT2114/mushroom-yield-project.git
cd mushroom-yield-project
```

Create and activate a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

### Run Environment Validation

```bash
python src/smoke_test.py
```

### Expected Output

```text
Polyhouse sensor snapshot:
...
Smoke Test Passed!
```

---

## Workflow

1. Store raw sensor files inside `data/raw/`
2. Clean and transform data into `data/processed/`
3. Perform analysis using notebooks
4. Train machine learning models
5. Save trained models in `models/`
6. Evaluate and deploy prediction pipeline

---

## Future Enhancements

* Automated data ingestion
* Feature engineering pipeline
* Hyperparameter tuning
* Streamlit dashboard
* Real-time sensor monitoring
* Cloud deployment



B.Tech Computer Science Engineering
AI & Data Analytics Project
