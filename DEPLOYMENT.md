# Public deployment and verification

**Public app:** https://mit105-airaware-ai-sdg11.streamlit.app/  
**Repository:** https://github.com/gurkiratjanjua13-creator/MIT105-AirAware-AI-SDG11  
**Entrypoint:** `main` branch, `app.py`  
**Evidence date:** 27 October 2026 (user-supplied browser test and screenshot)

## Recorded functional test

- Enter lag1 = 75, lag2 = 70, lag7 = 65 and rolling7 = 70 µg/m³.
- Select forecast date 27 October 2026.
- Select **Forecast next-day PM2.5**. The recorded interface output was **67.8 µg/m³**.
- The metrics table displayed Ridge holdout MAE **26.383**, RMSE **35.077**, R² **0.375**. Random forest and gradient boosting results are in `real_model_metrics.csv`.
- This verifies the reported application demonstration, **not** a measured pollution reading, ground-station validation or guaranteed future accuracy.

## Redeployment or repeat verification

1. Confirm `app.py`, `airaware_real_model.joblib`, `real_model_metrics.csv` and `requirements.txt` exist in the repository root.
2. Sign in to https://share.streamlit.io with GitHub and select the repository, branch `main` and entrypoint `app.py`.
3. Open the public URL, enter the four historical values, choose the forecast date and click the forecast button.
4. Check the resulting value and three-model evaluation table; save a dated screenshot if submitting new evidence.
5. If the environment changes, inspect deployment logs and dependency versions. Only load the trusted project joblib artifact.

## Data and integrity limitations

The source is 2025 Delhi Open-Meteo/CAMS **modelled** PM2.5, not ground-station observations. Historical lag inputs are entered manually; there is no automated real-time ingestion, regulatory warning service or independent station-based accuracy certification. The 67.8 µg/m³ figure is a demonstration prediction for the supplied inputs, not an observed value.
