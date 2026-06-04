## Problem Statement 
Predicting daily mushroom yield (kg) in a climate-controlled polyhouse using real-world sensor 
readings for temperature (°C), relative humidity (%), and CO₂ (ppm). This repository serves as a 
version-controlled data pipeline resilient against model breakdown due to sudden hardware or 
data drift updates. 
## Project Structure 
```text 
├── data/ 
│   ├── processed/        
│   └── raw/              
├── models/               
├── notebooks/            
├── src/ 
# Standardized datasets ready for modeling 
# Raw sensor data uploads (Excluded from Git) 
# Serialized production-ready model files 
# Jupyter notebooks for exploratory data analysis 
│   └── smoke_test.py     # Base validation environment script 
├── .gitignore            
# Explicitly excludes environment and large log assets 
├── README.md             
└── requirements.txt      
# Project roadmap and run protocols 
# Pinned infrastructure dependencies 

## Data Cleaning Strategy Log (Phase 1, Task 2)

**1. Outliers & Anomalies (Threshold Rules)**
Filtered humidity (50-100%), temperature (10-35°C), and CO2 (400-2000 ppm) to remove hard sensor failures (e.g., a dead humidity probe reading 0% or environmental spikes outside biological survival ranges). 

**2. Missing Values (Imputation vs. Row Removal)**
Handled short sensor dropouts (power blips, calibration gaps) using forward-fill (`ffill`) with a strict limit of 2 periods, assuming short-term microclimate stability. Rows completely missing the `yield_kg` target variable were dropped entirely, as we cannot train or evaluate models on missing ground-truth labels.

**3. Duplicates**
Removed exact timestamp duplicates, keeping the `last` entry under the assumption it represents the most recent or corrected system export.


# Data Cleaning Strategy & Log

## Missing Values
* **Initial Report:** Printed and reviewed prior to pipeline execution.
* **Sensor Gaps:** Short gaps (limit=2) in `temperature_c`, `humidity_pct`, and `co2_ppm` were imputed using forward-fill (`ffill`), assuming short-term MCAR dropouts (e.g., power blips).
* **Target Variable:** Rows with missing `yield_kg` after forward-filling were explicitly dropped.

## Outliers & Anomalies
* **Threshold Filters:** Applied explicit bounding rules for an oyster mushroom polyhouse. Readings outside these ranges were treated as sensor failures (e.g., dead probes) rather than rare microclimate events.
* **Ranges:** Humidity (50-100%), Temperature (10-35°C), CO2 (400-2000 ppm). 

## Duplicates
* **Resolution:** Duplicate timestamps, likely caused by double exports, were removed. The `last` recorded reading for any duplicate timestamp was kept.