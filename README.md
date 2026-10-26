# AirAware AI — MIT 105 Assessment 2 (SDG 11)

**Delhi next-day PM2.5 forecasting | Real-world-source 2025 Open-Meteo/CAMS air-quality estimates**

Group: Vishal (MLB0000808), Gurkirat Singh (MLB0000715), Harsh (MLB0000799).

## Reproducibility
The research compares Ridge regression, Random Forest, and Gradient Boosting using chronological holdout testing and time-series cross-validation. Data are CAMS-modelled estimates, **not** ground-station observations. The tested Ridge model achieved holdout MAE 26.383 µg/m³, RMSE 35.077 µg/m³, R² 0.375 (286 train / 72 test daily samples).

## Deployment
This repository will host the Streamlit app at `app.py`. Upload the matching `airaware_real_model.joblib`, `real_model_metrics.csv`, and `requirements.txt` from the validated submission project before deploying. In Streamlit Community Cloud, choose this repo, `main` branch and `app.py` entry point.

## Limitations
Forecasts are educational estimates, not regulatory air-quality alerts or medical advice. Localhost is not a public deployment. No live URL is claimed until Streamlit deployment is verified.

## References
- [Open-Meteo Air Quality API](https://open-meteo.com/en/docs/air-quality-api)
- [UN SDG 11](https://sdgs.un.org/goals/goal11)
- [Streamlit deployment documentation](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app)
