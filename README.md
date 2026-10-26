# AirAware AI | MIT 105 Assessment 2

**Explainable next-day PM2.5 forecasting for Delhi · UN SDG 11: Sustainable Cities and Communities**

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B)](https://streamlit.io/)
[![Project](https://img.shields.io/badge/Status-Research%20Prototype-16A6A1)](#limitations-and-integrity)
[![SDG](https://img.shields.io/badge/UN%20SDG-11-orange)](https://sdgs.un.org/goals/goal11)

> **Deployment status:** GitHub source and trained model available. Public Streamlit URL has not yet been verified; do not mistake this repository or localhost for public deployment.

## Project overview

AirAware AI estimates next-day daily PM2.5 concentration using previous-day concentration history and calendar features. It is an academic prototype supporting SDG target 11.6 by exploring accessible air-quality decision support. It is **not** a regulatory, health-advice or emergency-warning service.

**Team:** Vishal (MLB0000808) · Gurkirat Singh (MLB0000715) · Harsh (MLB0000799)  
**Course:** MIT 105 Data Analytics · Assessment 2, Group Project: Applied Analytical Strategies.

## Results: 2025 Delhi CAMS-modelled estimates

| Model | Holdout MAE ↓ | Holdout RMSE ↓ | Holdout R² ↑ | Training CV MAE ↓ |
|---|---:|---:|---:|---:|
| **Ridge regression** | **26.383** | **35.077** | **0.375** | 17.794 |
| Random forest | 28.273 | 39.107 | 0.223 | **12.826** |
| Gradient boosting | 30.586 | 43.010 | 0.060 | 14.975 |

Metrics are computed on a **chronological holdout** of 72 daily records, after training on 286 earlier daily records. Ridge was selected by holdout MAE. Training-only time-series CV favoured random forest; this difference is discussed as a robustness limitation. The 2025 hourly input covers 8,760 records; daily lag creation leaves 358 modelled days.

**Important provenance:** Source is the Open-Meteo Air Quality API's **CAMS-modelled estimates**, not direct monitoring-station observations. Values must not be described as ground-truth measurements.

## Methodology

```text
Open-Meteo / CAMS hourly data (Delhi, 2025)
        │
        ▼
Clean, sort, aggregate to daily PM2.5
        │
        ▼
Create historical features: lag1, lag2, lag7,
rolling7, dayofyear, month
        │
        ▼
Chronological 80/20 train–test split
        │
        ├── Ridge regression
        ├── Random forest
        └── Histogram gradient boosting
        │
        ▼
4-fold time-series CV on training portion
+ final holdout MAE, RMSE and R²
        │
        ▼
Select Ridge → trusted joblib model → Streamlit UI
```

Same-day PM10 and NO₂ are deliberately excluded from predictors because they would be unavailable at forecast time. This avoids one common form of look-ahead leakage.

## Run locally

```bash
python -m venv .venv
# Activate the virtual environment for your OS.
python -m pip install -r requirements.txt
streamlit run app.py
```

The repository includes the fitted model and evaluation metrics, so **downloading data or retraining is not necessary to launch the app**.

To reproduce the experiment from the external API:

```bash
python fetch_real_air_quality.py
python train_real_models.py
```

The scripts create the source CSV, holdout predictions, metrics, model and experiment manifest. The API may revise historical estimates; reruns may differ from the archived reported results.

Run lightweight repository checks:

```bash
python -m pip install pytest
python -m pytest -q
```

## Repository guide

| File | Purpose |
|---|---|
| `app.py` | Streamlit inference and results dashboard |
| `airaware_real_model.joblib` | Fitted Ridge pipeline; trusted project artifact |
| `real_model_metrics.csv` | Three-model holdout/CV summary |
| `fetch_real_air_quality.py` | Reproducible API data acquisition |
| `train_real_models.py` | Preprocessing, three-model training and evaluation |
| `real_experiment_manifest.json` | Source, data type, split and metrics |
| `tests/test_project.py` | Minimal artifact/metric consistency checks |
| `.streamlit/config.toml` | Consistent dashboard theme |
| `DEPLOYMENT.md` | Step-by-step public deployment and verification |
| `requirements.txt` | Runtime and research dependencies |

**Submission files are intentionally kept outside this source repository.** The Moodle/Turnitin submission bundle contains the report (DOCX/PDF) and presentation only.

## Public deployment

Follow [DEPLOYMENT.md](DEPLOYMENT.md) to deploy `main:app.py` using Streamlit Community Cloud. After deploying, record the public URL and evidence screenshots in the assessment documents. Do not publish private credentials.

## Limitations and integrity

- This is an educational, city-level modelling demonstration, not a production forecast service.
- No independent ground-monitor validation, calibrated uncertainty interval or external-city generalisation has been demonstrated.
- The user supplies historical lag features manually; the app does not automatically retrieve live pollution measurements.
- Meeting records and simulated market interviews must not be represented as actual participant testimony unless verified.
- The model artifact is serialized with joblib; **only load trusted files** and use a compatible scikit-learn version.

## References

- [UN SDG 11](https://sdgs.un.org/goals/goal11)
- [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api)
- [Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app)
- [scikit-learn time-series cross-validation](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)
