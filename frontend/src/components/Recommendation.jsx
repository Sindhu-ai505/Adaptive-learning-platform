import React from "react";

const levelIcon = { beginner: "🌱", intermediate: "🌿", advanced: "🌳" };
const levelColor = { beginner: "#15803d", intermediate: "#854d0e", advanced: "#1d4ed8" };

export default function Recommendation({ data }) {
  if (!data) return null;

  const icon = levelIcon[data.level] || "📊";
  const color = levelColor[data.level] || "#4f46e5";

  return (
    <div className="card" style={styles.card}>
      <div style={styles.header}>
        <span style={styles.icon}>{icon}</span>
        <div>
          <p style={styles.label}>Your Level</p>
          <p style={{ ...styles.level, color }}>{data.level}</p>
        </div>
        <div style={styles.scoreBox}>
          <p style={styles.label}>Score</p>
          <p style={{ ...styles.score, color }}>{data.score}%</p>
        </div>
      </div>

      {data.recommendation && (
        <div style={styles.rec}>
          <p style={styles.recTitle}>📌 Recommendation</p>
          <p style={styles.recText}>{data.recommendation}</p>
        </div>
      )}

      <div style={styles.stats}>
        <Stat label="Correct" value={data.correct_answers} color="#22c55e" />
        <Stat label="Total" value={data.total_questions} color="#64748b" />
        <Stat label="Next" value={data.recommendation_type} color="#4f46e5" />
      </div>
    </div>
  );
}

function Stat({ label, value, color }) {
  return (
    <div style={styles.stat}>
      <span style={{ ...styles.statVal, color }}>{value}</span>
      <span style={styles.statLabel}>{label}</span>
    </div>
  );
}

const styles = {
  card: { display: "flex", flexDirection: "column", gap: "1rem" },
  header: { display: "flex", alignItems: "center", gap: "1rem" },
  icon: { fontSize: "2.5rem" },
  label: { fontSize: "0.75rem", color: "#64748b", textTransform: "uppercase", fontWeight: 600 },
  level: { fontSize: "1.1rem", fontWeight: 700, textTransform: "capitalize" },
  scoreBox: { marginLeft: "auto", textAlign: "right" },
  score: { fontSize: "1.5rem", fontWeight: 800 },
  rec: {
    background: "#f8fafc",
    border: "1px solid #e2e8f0",
    borderRadius: "0.375rem",
    padding: "0.75rem 1rem",
  },
  recTitle: { fontWeight: 700, fontSize: "0.85rem", marginBottom: "0.25rem", color: "#1e293b" },
  recText: { fontSize: "0.875rem", color: "#475569", lineHeight: 1.6 },
  stats: { display: "flex", gap: "1.5rem" },
  stat: { display: "flex", flexDirection: "column", alignItems: "center", gap: "0.1rem" },
  statVal: { fontSize: "1.2rem", fontWeight: 700 },
  statLabel: { fontSize: "0.72rem", color: "#94a3b8", textTransform: "uppercase", fontWeight: 600 },
};
