import React from "react";
import { useNavigate } from "react-router-dom";

export default function ATTutor() {
  const navigate = useNavigate();
  return (
    <main style={{ maxWidth: 600, margin: "4rem auto", padding: "0 1.25rem", textAlign: "center", display: "flex", flexDirection: "column", gap: "1rem", alignItems: "center" }}>
      <span style={{ fontSize: "4rem" }}>🤖</span>
      <h1 style={{ fontSize: "1.5rem", fontWeight: 800, color: "#1e293b" }}>AT Tutor</h1>
      <p style={{ color: "#64748b" }}>
        The interactive AI tutor is coming soon. For now, use the Recommendations page to get AI-generated feedback after each quiz.
      </p>
      <button className="btn btn-primary" onClick={() => navigate("/recommendations")}>
        Go to Recommendations →
      </button>
    </main>
  );
}
