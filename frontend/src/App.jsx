import axios from "axios";
import { useState } from "react";
import PredictionForm from "./PredictionForm.jsx";
import ResultChart from "./ResultChart.jsx";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(formData) {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await axios.post(`${API_URL}/predict`, formData);
      setResult(res.data);
    } catch (err) {
      setError(
        err.response?.data?.detail || "Something went wrong while predicting. Is the API running?"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header>
        <h1>Student Performance Predictor</h1>
        <p>
          Enter a student's academic and social profile to predict their final
          grade (G3, out of 20), trained on the UCI Student Performance dataset.
        </p>
      </header>

      <main>
        <PredictionForm onSubmit={handleSubmit} loading={loading} />
        {error && <div className="error">{error}</div>}
        <ResultChart result={result} />
      </main>

      <footer>
        <p>Model: Random Forest Regressor · scikit-learn · FastAPI · React</p>
      </footer>
    </div>
  );
}
