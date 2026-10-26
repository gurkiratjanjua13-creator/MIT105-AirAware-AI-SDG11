"""Reproduce the 2025 Delhi PM2.5 chronological model comparison."""
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit

BASE = Path(__file__).resolve().parent
p = BASE / "real_cams_air_quality_2025_delhi.csv"
if not p.exists():
    raise SystemExit("Dataset missing. Run fetch_real_air_quality.py first.")
raw = pd.read_csv(p, parse_dates=["time"]).sort_values("time").drop_duplicates("time")
daily = raw.set_index("time").resample("D").agg({"pm2_5": "mean", "pm10": "mean", "nitrogen_dioxide": "mean"})
daily = daily.dropna(subset=["pm2_5"])
daily["lag1"] = daily.pm2_5.shift(1)
daily["lag2"] = daily.pm2_5.shift(2)
daily["lag7"] = daily.pm2_5.shift(7)
daily["rolling7"] = daily.pm2_5.shift(1).rolling(7).mean()
daily["dayofyear"] = daily.index.dayofyear
daily["month"] = daily.index.month
features = ["lag1", "lag2", "lag7", "rolling7", "dayofyear", "month"]
daily = daily.dropna(subset=features)
cut = int(len(daily) * 0.8)
train, test = daily.iloc[:cut], daily.iloc[cut:]
Xtr, Xte = train[features], test[features]
ytr, yte = train.pm2_5, test.pm2_5
models = {
    "Ridge": make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), Ridge(alpha=10)),
    "Random forest": RandomForestRegressor(n_estimators=250, min_samples_leaf=3, random_state=42, n_jobs=-1),
    "Gradient boosting": HistGradientBoostingRegressor(max_iter=200, l2_regularization=10, random_state=42),
}
results = []
predictions = pd.DataFrame({"date": test.index.astype(str), "actual_pm25": yte.to_numpy()})
for name, model in models.items():
    model.fit(Xtr, ytr)
    yhat = model.predict(Xte)
    cv_mae = []
    for a, b in TimeSeriesSplit(n_splits=4).split(Xtr):
        model.fit(Xtr.iloc[a], ytr.iloc[a])
        cv_mae.append(mean_absolute_error(ytr.iloc[b], model.predict(Xtr.iloc[b])))
    model.fit(Xtr, ytr)
    results.append({"model": name, "MAE": round(mean_absolute_error(yte, yhat), 3),
                    "RMSE": round(np.sqrt(mean_squared_error(yte, yhat)), 3),
                    "R2": round(r2_score(yte, yhat), 3),
                    "CV_MAE_mean": round(float(np.mean(cv_mae)), 3)})
    predictions[name.lower().replace(" ", "_")] = yhat
pd.DataFrame(results).to_csv(BASE / "real_model_metrics.csv", index=False)
predictions.to_csv(BASE / "real_holdout_predictions.csv", index=False)
winner = min(results, key=lambda r: r["MAE"])["model"]
joblib.dump({"name": winner, "model": models[winner], "features": features,
             "data_provenance": "Open-Meteo CAMS-modelled Delhi 2025 daily aggregates"},
            BASE / "airaware_real_model.joblib")
manifest = {"source": "https://air-quality-api.open-meteo.com/v1/air-quality",
            "location": "Delhi 28.6139,77.2090", "period": "2025-01-01 to 2025-12-31",
            "data_type": "CAMS modelled, not ground-station observations",
            "train_days": len(train), "test_days": len(test),
            "selected_model": winner, "metrics": results}
(BASE / "real_experiment_manifest.json").write_text(json.dumps(manifest, indent=2))
print(pd.DataFrame(results).to_string(index=False))
