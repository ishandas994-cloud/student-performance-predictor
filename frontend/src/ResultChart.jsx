import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export default function ResultChart({ result }) {
  if (!result) return null;

  const { predicted_g3, predicted_grade_percent, pass_fail, top_features } = result;
  const chartData = top_features.map((f) => ({
    name: f.feature,
    importance: Number((f.importance * 100).toFixed(1)),
  }));

  return (
    <div className="result">
      <div className={`score-card ${pass_fail === "Pass" ? "pass" : "fail"}`}>
        <div className="score-value">{predicted_g3} / 20</div>
        <div className="score-percent">{predicted_grade_percent}%</div>
        <div className="score-status">{pass_fail}</div>
      </div>

      {chartData.length > 0 && (
        <div className="chart-wrapper">
          <h3>What drove this prediction</h3>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={chartData} layout="vertical" margin={{ left: 24 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" unit="%" />
              <YAxis type="category" dataKey="name" width={90} />
              <Tooltip formatter={(value) => [`${value}%`, "Importance"]} />
              <Bar dataKey="importance" fill="#4f46e5" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
