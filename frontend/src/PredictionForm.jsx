import { useState } from "react";

const DEFAULTS = {
  age: 17, Medu: 3, Fedu: 2, traveltime: 1, studytime: 2,
  failures: 0, famrel: 4, freetime: 3, goout: 3, Dalc: 1,
  Walc: 2, health: 4, absences: 4, G1: 14, G2: 15,
  school: "GP", sex: "F", address: "U", famsize: "GT3",
  Pstatus: "T", Mjob: "teacher", Fjob: "other", reason: "course",
  guardian: "mother", schoolsup: "no", famsup: "yes", paid: "no",
  activities: "yes", nursery: "yes", higher: "yes",
  internet: "yes", romantic: "no",
};

const YES_NO_FIELDS = [
  "schoolsup", "famsup", "paid", "activities", "nursery", "higher",
  "internet", "romantic",
];

const NUMBER_FIELDS = [
  { name: "age", label: "Age", min: 15, max: 22 },
  { name: "Medu", label: "Mother's education (0-4)", min: 0, max: 4 },
  { name: "Fedu", label: "Father's education (0-4)", min: 0, max: 4 },
  { name: "traveltime", label: "Travel time to school (1-4)", min: 1, max: 4 },
  { name: "studytime", label: "Weekly study time (1-4)", min: 1, max: 4 },
  { name: "failures", label: "Past class failures (0-4)", min: 0, max: 4 },
  { name: "famrel", label: "Family relationship quality (1-5)", min: 1, max: 5 },
  { name: "freetime", label: "Free time after school (1-5)", min: 1, max: 5 },
  { name: "goout", label: "Going out with friends (1-5)", min: 1, max: 5 },
  { name: "Dalc", label: "Workday alcohol use (1-5)", min: 1, max: 5 },
  { name: "Walc", label: "Weekend alcohol use (1-5)", min: 1, max: 5 },
  { name: "health", label: "Current health (1-5)", min: 1, max: 5 },
  { name: "absences", label: "School absences", min: 0, max: 100 },
  { name: "G1", label: "First period grade (0-20)", min: 0, max: 20 },
  { name: "G2", label: "Second period grade (0-20)", min: 0, max: 20 },
];

export default function PredictionForm({ onSubmit, loading }) {
  const [form, setForm] = useState(DEFAULTS);

  function update(name, value) {
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  function handleNumberChange(name, e) {
    update(name, e.target.value === "" ? "" : Number(e.target.value));
  }

  function handleSubmit(e) {
    e.preventDefault();
    onSubmit(form);
  }

  return (
    <form className="predict-form" onSubmit={handleSubmit}>
      <fieldset>
        <legend>Academic factors</legend>
        <div className="grid">
          {NUMBER_FIELDS.map(({ name, label, min, max }) => (
            <label key={name}>
              {label}
              <input
                type="number"
                min={min}
                max={max}
                value={form[name]}
                onChange={(e) => handleNumberChange(name, e)}
                required
              />
            </label>
          ))}
        </div>
      </fieldset>

      <fieldset>
        <legend>Background</legend>
        <div className="grid">
          <label>
            School
            <select value={form.school} onChange={(e) => update("school", e.target.value)}>
              <option value="GP">Gabriel Pereira</option>
              <option value="MS">Mousinho da Silveira</option>
            </select>
          </label>
          <label>
            Sex
            <select value={form.sex} onChange={(e) => update("sex", e.target.value)}>
              <option value="F">Female</option>
              <option value="M">Male</option>
            </select>
          </label>
          <label>
            Address
            <select value={form.address} onChange={(e) => update("address", e.target.value)}>
              <option value="U">Urban</option>
              <option value="R">Rural</option>
            </select>
          </label>
          <label>
            Family size
            <select value={form.famsize} onChange={(e) => update("famsize", e.target.value)}>
              <option value="LE3">3 or fewer</option>
              <option value="GT3">More than 3</option>
            </select>
          </label>
          <label>
            Parents' cohabitation
            <select value={form.Pstatus} onChange={(e) => update("Pstatus", e.target.value)}>
              <option value="T">Living together</option>
              <option value="A">Apart</option>
            </select>
          </label>
          <label>
            Mother's job
            <select value={form.Mjob} onChange={(e) => update("Mjob", e.target.value)}>
              {["teacher", "health", "services", "at_home", "other"].map((v) => (
                <option key={v} value={v}>{v}</option>
              ))}
            </select>
          </label>
          <label>
            Father's job
            <select value={form.Fjob} onChange={(e) => update("Fjob", e.target.value)}>
              {["teacher", "health", "services", "at_home", "other"].map((v) => (
                <option key={v} value={v}>{v}</option>
              ))}
            </select>
          </label>
          <label>
            Reason for choosing school
            <select value={form.reason} onChange={(e) => update("reason", e.target.value)}>
              {["home", "reputation", "course", "other"].map((v) => (
                <option key={v} value={v}>{v}</option>
              ))}
            </select>
          </label>
          <label>
            Guardian
            <select value={form.guardian} onChange={(e) => update("guardian", e.target.value)}>
              {["mother", "father", "other"].map((v) => (
                <option key={v} value={v}>{v}</option>
              ))}
            </select>
          </label>
        </div>
      </fieldset>

      <fieldset>
        <legend>Support & lifestyle</legend>
        <div className="grid checkboxes">
          {YES_NO_FIELDS.map((name) => (
            <label key={name} className="checkbox">
              <input
                type="checkbox"
                checked={form[name] === "yes"}
                onChange={(e) => update(name, e.target.checked ? "yes" : "no")}
              />
              {name}
            </label>
          ))}
        </div>
      </fieldset>

      <button type="submit" disabled={loading}>
        {loading ? "Predicting..." : "Predict final grade"}
      </button>
    </form>
  );
}
