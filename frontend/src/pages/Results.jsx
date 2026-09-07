import React, { useEffect, useState } from "react";
import { useParams, useLocation, useNavigate } from "react-router-dom";
import { attemptsApi, recommendationsApi } from "../services/api";
import { useAuth } from "../context/useAuth";
import Recommendation from "../components/Recommendation";

export default function Results() {
  const { attemptId } = useParams();
  const { state } = useLocation();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [attempt, setAttempt] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const { data: attemptData } = await attemptsApi.get(attemptId);
        setAttempt(attemptData.attempt);

        // Fetch recommendation if we know the quizId
        const quizId = state?.quizId || attemptData.attempt?.quiz_id;
        if (quizId) {
          try {
            const { data: rec } = await recommendationsApi.get(user.id, quizId);
            setRecommendation(rec);
          } catch {
            // Recommendations might not be available — that's ok
          }
        }
      } catch {
        setError("Could not load results.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [attemptId, user.id, state?.quizId]);

  if (loading) return <div style={styles.main}><div className="spinner" /></div>;
  if (error) return <div style={styles.main}><div className="error-msg">{error}</div></div>;

  const score = attempt?.score ?? 0;
  const correct = attempt?.correct_answers ?? 0;
  const total = attempt?.total_questions ?? 0;

  const emoji = score >= 70 ? "🎉" : score >= 40 ? "👍" : "📖";
  const msg =
    score >= 70 ? "Excellent work!" : score >= 40 ? "Good effort!" : "Keep practicing!";

  return (
    <main style={styles.main}>
      {/* Score card */}
      <div className="card" style={styles.scoreCard}>
        <div style={styles.emoji}>{emoji}</div>
        <h1 style={styles.msg}>{msg}</h1>
        <div style={styles.bigScore}>{Math.round(score)}%</div>
        <p style={styles.detail}>{correct} correct out of {total} questions</p>

        {/* Score bar */}
        <div style={styles.barBg}>
          <div
            style={{
              ...styles.barFill,
              width: `${score}%`,
              background: score >= 70 ? "#22c55e" : score >= 40 ? "#f59e0b" : "#ef4444",
            }}
          />
        </div>
      </div>

      {/* Stats row */}
      <div style={styles.statsRow}>
        <StatBox icon="✅" label="Correct" value={correct} color="#22c55e" />
        <StatBox icon="❌" label="Incorrect" value={total - correct} color="#ef4444" />
        <StatBox icon="📊" label="Score" value={`${Math.round(score)}%`} color="#4f46e5" />
      </div>

      {/* Recommendation */}
      {recommendation && (
        <section>
          <h2 style={styles.sectionTitle}>Your Personalised Recommendation</h2>
          <Recommendation data={recommendation} />
        </section>
      )}

      {/* Actions */}
      <div style={styles.actions}>
        <button className="btn btn-outline" onClick={() => navigate("/courses")}>
          ← Back to Courses
        </button>
        <button className="btn btn-primary" onClick={() => navigate("/recommendations")}>
          💡 View Recommendations
        </button>
        <button className="btn btn-secondary" onClick={() => navigate("/dashboard")}>
          🏠 Dashboard
        </button>
      </div>
    </main>
  );
}

function StatBox({ icon, label, value, color }) {
  return (
    <div className="card" style={{ textAlign: "center", flex: 1 }}>
      <div style={{ fontSize: "1.5rem" }}>{icon}</div>
      <div style={{ fontSize: "1.6rem", fontWeight: 800, color }}>{value}</div>
      <div style={{ fontSize: "0.75rem", color: "#64748b", textTransform: "uppercase", fontWeight: 600 }}>{label}</div>
    </div>
  );
}

const styles = {
  main: { maxWidth: 700, margin: "0 auto", padding: "2rem 1.25rem", display: "flex", flexDirection: "column", gap: "1.5rem" },
  scoreCard: { textAlign: "center", display: "flex", flexDirection: "column", alignItems: "center", gap: "0.75rem", padding: "2.5rem" },
  emoji: { fontSize: "4rem" },
  msg: { fontSize: "1.5rem", fontWeight: 800, color: "#1e293b" },
  bigScore: { fontSize: "4rem", fontWeight: 900, color: "#4f46e5", lineHeight: 1 },
  detail: { color: "#64748b", fontSize: "0.9rem" },
  barBg: { width: "100%", height: 10, background: "#e2e8f0", borderRadius: 99, overflow: "hidden", maxWidth: 400 },
  barFill: { height: "100%", borderRadius: 99, transition: "width 0.6s ease" },
  statsRow: { display: "flex", gap: "1rem", flexWrap: "wrap" },
  sectionTitle: { fontSize: "1.1rem", fontWeight: 700, color: "#1e293b", marginBottom: "0.75rem" },
  actions: { display: "flex", gap: "0.75rem", flexWrap: "wrap", justifyContent: "center" },
};
