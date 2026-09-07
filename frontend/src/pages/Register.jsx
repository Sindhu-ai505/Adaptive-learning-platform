import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/useAuth";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    learning_level: "beginner",
    learning_style: "visual",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(e) {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await register(form);
      navigate("/login", { state: { registered: true } });
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed. Try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.page}>
      <div style={styles.card} className="card">
        <div style={styles.logo}>🎓</div>
        <h1 style={styles.title}>Create an account</h1>
        <p style={styles.sub}>Start your adaptive learning journey</p>

        {error && <div className="error-msg">{error}</div>}

        <form onSubmit={handleSubmit} style={styles.form} noValidate>
          <label style={styles.label}>
            Full name
            <input name="name" value={form.name} onChange={handleChange} required style={styles.input} placeholder="Jane Doe" />
          </label>

          <label style={styles.label}>
            Email
            <input type="email" name="email" value={form.email} onChange={handleChange} required style={styles.input} placeholder="you@example.com" />
          </label>

          <label style={styles.label}>
            Password
            <input type="password" name="password" value={form.password} onChange={handleChange} required style={styles.input} placeholder="Min. 8 characters" />
          </label>

          <div style={styles.row}>
            <label style={styles.label}>
              Learning level
              <select name="learning_level" value={form.learning_level} onChange={handleChange} style={styles.input}>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </label>

            <label style={styles.label}>
              Learning style
              <select name="learning_style" value={form.learning_style} onChange={handleChange} style={styles.input}>
                <option value="visual">Visual</option>
                <option value="auditory">Auditory</option>
                <option value="reading">Reading</option>
                <option value="kinesthetic">Kinesthetic</option>
              </select>
            </label>
          </div>

          <button type="submit" className="btn btn-primary" style={styles.btn} disabled={loading}>
            {loading ? "Creating account…" : "Create account"}
          </button>
        </form>

        <p style={styles.footer}>
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "linear-gradient(135deg, #eef2ff 0%, #f8fafc 100%)",
    padding: "1rem",
  },
  card: { width: "100%", maxWidth: 460, display: "flex", flexDirection: "column", gap: "1rem" },
  logo: { fontSize: "2.5rem", textAlign: "center" },
  title: { fontSize: "1.6rem", fontWeight: 800, textAlign: "center", color: "#1e293b" },
  sub: { fontSize: "0.875rem", color: "#64748b", textAlign: "center", marginTop: "-0.5rem" },
  form: { display: "flex", flexDirection: "column", gap: "0.9rem" },
  row: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.75rem" },
  label: { display: "flex", flexDirection: "column", gap: "0.3rem", fontSize: "0.875rem", fontWeight: 600, color: "#374151" },
  input: {
    padding: "0.6rem 0.8rem",
    border: "1.5px solid #e2e8f0",
    borderRadius: "0.4rem",
    fontSize: "0.9rem",
    outline: "none",
    background: "#fff",
  },
  btn: { width: "100%", padding: "0.7rem", fontSize: "1rem" },
  footer: { textAlign: "center", fontSize: "0.875rem", color: "#64748b" },
};
