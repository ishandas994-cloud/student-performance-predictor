# Student Performance Predictor

Predicts a student's final grade (G3, 0–20) from academic and social
factors, trained on the UCI "Student Performance" dataset (Cortez & Silva,
2008). Full-stack: scikit-learn model → FastAPI → React UI.

## Results

| Model              | RMSE | MAE  | R²   |
|---------------------|------|------|------|
| Linear Regression   | 2.38 | 1.65 | 0.72 |
| Random Forest        | **2.01** | **1.19** | **0.80** |

Random Forest was selected. The single strongest predictor is `G2` (second
period grade), followed by `absences` — consistent with the dataset's known
finding that continuous assessment strongly predicts the final result.

## Structure

```
ml/         Training script + dataset (student-mat.csv) + saved model
backend/    FastAPI service exposing POST /predict
frontend/   React UI (Vite) — form in, prediction + feature-importance chart out
```

## Running locally

**1. Train the model** (already done — `ml/model.pkl` is included, re-run to regenerate):
```bash
cd ml
pip install -r ../backend/requirements.txt
python train.py
```

**2. Start the API**:
```bash
cd backend
cp ../ml/model.pkl ../ml/metrics.json .
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Visit `http://localhost:8000/docs` for interactive API docs.

**3. Start the frontend**:
```bash
cd frontend
npm install
npm run dev
```
Visit `http://localhost:5173`. Set `VITE_API_URL` in a `.env` file if your
API isn't on `localhost:8000`.

## Deployment

- **Backend**: Render or Railway (needs a Python runtime — Vercel's Python
  support doesn't handle scikit-learn well). Point the start command at
  `uvicorn main:app --host 0.0.0.0 --port $PORT`.
- **Frontend**: Vercel, with `VITE_API_URL` set to your deployed backend URL.

## Dataset

UCI Student Performance Dataset — 395 students, Math course, Portuguese
secondary schools. https://archive.ics.uci.edu/dataset/320/student+performance

Citation: P. Cortez and A. Silva. *Using Data Mining to Predict Secondary
School Student Performance.* FUBUTEC 2008.
