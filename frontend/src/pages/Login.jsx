import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState({ email: "", password: "" });
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
      await login(form.email, form.password);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed. Check your credentials.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.page}>
      <div style={styles.card} className="card">
        <div style={styles.logo}>🎓</div>
        <h1 style={styles.title}>Welcome back</h1>
        <p style={styles.sub}>Sign in to your AdaptiveLearn account</p>

        {error && <div className="error-msg">{error}</div>}

        <form onSubmit={handleSubmit} style={styles.form} noValidate>
          <label style={styles.label}>
            Email
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              required
              autoComplete="email"
              style={styles.input}
              placeholder="you@example.com"
            />
          </label>

          <label style={styles.label}>
            Password
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              required
              autoComplete="current-password"
              style={styles.input}
              placeholder="••••••••"
            />
          </label>

          <button type="submit" className="btn btn-primary" style={styles.btn} disabled={loading}>
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>

        <p style={styles.footer}>
          Don&apos;t have an account?{" "}
          <Link to="/register">Create one</Link>
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
  card: { width: "100%", maxWidth: 420, display: "flex", flexDirection: "column", gap: "1rem" },
  logo: { fontSize: "2.5rem", textAlign: "center" },
  title: { fontSize: "1.6rem", fontWeight: 800, textAlign: "center", color: "#1e293b" },
  sub: { fontSize: "0.875rem", color: "#64748b", textAlign: "center", marginTop: "-0.5rem" },
  form: { display: "flex", flexDirection: "column", gap: "1rem" },
  label: { display: "flex", flexDirection: "column", gap: "0.3rem", fontSize: "0.875rem", fontWeight: 600, color: "#374151" },
  input: {
    padding: "0.6rem 0.8rem",
    border: "1.5px solid #e2e8f0",
    borderRadius: "0.4rem",
    fontSize: "0.95rem",
    outline: "none",
    transition: "border-color 0.2s",
  },
  btn: { width: "100%", padding: "0.7rem", fontSize: "1rem" },
  footer: { textAlign: "center", fontSize: "0.875rem", color: "#64748b" },
};
