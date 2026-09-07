import React from "react";

export default function ProgressCard({ label, value, total, color = "#4f46e5" }) {
  const pct = total > 0 ? Math.round((value / total) * 100) : 0;

  return (
    <div className="card" style={styles.card}>
      <div style={styles.top}>
        <span style={styles.label}>{label}</span>
        <span style={{ ...styles.pct, color }}>{pct}%</span>
      </div>
      <div style={styles.barBg}>
        <div style={{ ...styles.barFill, width: `${pct}%`, background: color }} />
      </div>
      <div style={styles.sub}>
        {value} / {total}
      </div>
    </div>
  );
}

const styles = {
  card: { display: "flex", flexDirection: "column", gap: "0.5rem" },
  top: { display: "flex", justifyContent: "space-between", alignItems: "center" },
  label: { fontWeight: 600, fontSize: "0.9rem", color: "#1e293b" },
  pct: { fontWeight: 700, fontSize: "1.1rem" },
  barBg: {
    height: 8,
    background: "#e2e8f0",
    borderRadius: 99,
    overflow: "hidden",
  },
  barFill: {
    height: "100%",
    borderRadius: 99,
    transition: "width 0.5s ease",
  },
  sub: { fontSize: "0.78rem", color: "#64748b" },
};
