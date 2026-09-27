"""
train.py — Student Performance Predictor
Trains a regression model to predict a student's final grade (G3, 0-20)
from the UCI "Student Performance" dataset (student-mat.csv).

Run:
    python train.py

Outputs:
    model.pkl          — trained sklearn Pipeline (preprocessing + model)
    metrics.json        — evaluation metrics for the notebook/README
"""

import json
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

warnings.filterwarnings("ignore")

DATA_PATH = "data/student-mat.csv"
MODEL_PATH = "model.pkl"
METRICS_PATH = "metrics.json"
TARGET = "G3"

# Columns as documented by UCI: https://archive.ics.uci.edu/dataset/320
NUMERIC_FEATURES = [
    "age", "Medu", "Fedu", "traveltime", "studytime", "failures",
    "famrel", "freetime", "goout", "Dalc", "Walc", "health", "absences",
    "G1", "G2",
]
CATEGORICAL_FEATURES = [
    "school", "sex", "address", "famsize", "Pstatus", "Mjob", "Fjob",
    "reason", "guardian", "schoolsup", "famsup", "paid", "activities",
    "nursery", "higher", "internet", "romantic",
]


def load_data(path: str) -> pd.DataFrame:
    # The original UCI file is semicolon-separated with quoted values.
    df = pd.read_csv(path, sep=";")
    df.columns = [c.strip().strip('"') for c in df.columns]
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.strip().str.strip('"')
    # G1/G2/G3 are read as strings because of quoting in this mirror — coerce to numeric.
    for col in ["G1", "G2", "G3"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def build_pipeline(model) -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )
    return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])


def evaluate(y_true, y_pred) -> dict:
    return {
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
    }


def main():
    df = load_data(DATA_PATH)
    print(f"Loaded {len(df)} rows, {df.shape[1]} columns")

    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    candidates = {
        "linear_regression": build_pipeline(LinearRegression()),
        "random_forest": build_pipeline(
            RandomForestRegressor(n_estimators=300, max_depth=8, random_state=42)
        ),
    }

    results = {}
    fitted = {}
    for name, pipeline in candidates.items():
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)
        results[name] = evaluate(y_test, preds)
        fitted[name] = pipeline
        print(f"{name}: {results[name]}")

    best_name = min(results, key=lambda n: results[n]["rmse"])
    best_pipeline = fitted[best_name]
    print(f"\nBest model: {best_name} -> {results[best_name]}")

    # Feature importance (only meaningful for the random forest branch)
    feature_importance = None
    if best_name == "random_forest":
        ohe = best_pipeline.named_steps["preprocessor"].named_transformers_["cat"]
        cat_names = list(ohe.get_feature_names_out(CATEGORICAL_FEATURES))
        all_names = NUMERIC_FEATURES + cat_names
        importances = best_pipeline.named_steps["model"].feature_importances_
        feature_importance = sorted(
            zip(all_names, importances.tolist()), key=lambda t: -t[1]
        )[:10]

    joblib.dump(best_pipeline, MODEL_PATH)
    with open(METRICS_PATH, "w") as f:
        json.dump(
            {
                "best_model": best_name,
                "results": results,
                "top_features": feature_importance,
                "n_train": len(X_train),
                "n_test": len(X_test),
            },
            f,
            indent=2,
        )
    print(f"\nSaved {MODEL_PATH} and {METRICS_PATH}")


if __name__ == "__main__":
    main()
