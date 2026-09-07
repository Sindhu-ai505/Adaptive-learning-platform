import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { recommendationsApi, feedbackApi } from "../services/api";
import { useAuth } from "../context/useAuth";
import Recommendation from "../components/Recommendation";

export default function Recommendations() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [quizId, setQuizId] = useState("");
  const [recommendation, setRecommendation] = useState(null);
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(false);
  const [feedbackLoading, setFeedbackLoading] = useState(false);
  const [error, setError] = useState("");

  async function fetchRecommendation() {
    if (!quizId) return;
    setError("");
    setRecommendation(null);
    setFeedback("");
    setLoading(true);
    try {
      const { data } = await recommendationsApi.get(user.id, quizId);
      setRecommendation(data);
    } catch (err) {
      setError(err.response?.data?.detail || "No recommendation found for this quiz.");
    } finally {
      setLoading(false);
    }
  }

  async function fetchAIFeedback() {
    setFeedbackLoading(true);
    setFeedback("");
    try {
      const { data } = await feedbackApi.get(user.id, quizId);
      setFeedback(data.ai_feedback || "");
    } catch (err) {
      setFeedback(err.response?.data?.detail || "Could not generate AI feedback.");
    } finally {
      setFeedbackLoading(false);
    }
  }

  return (
    <main style={styles.main}>
      <div className="page-header">
        <h1>Recommendations</h1>
        <p>Enter a quiz ID to see your personalised performance analysis and AI feedback</p>
      </div>

      {/* Input */}
      <div className="card" style={styles.inputCard}>
        <label style={styles.label}>
          Quiz ID
          <div style={styles.inputRow}>
            <input
              type="number"
              min={1}
              value={quizId}
              onChange={(e) => setQuizId(e.target.value)}
              placeholder="e.g. 1"
              style={styles.input}
              onKeyDown={(e) => e.key === "Enter" && fetchRecommendation()}
            />
            <button
              className="btn btn-primary"
              onClick={fetchRecommendation}
              disabled={!quizId || loading}
            >
              {loading ? "Loading…" : "Analyse"}
            </button>
          </div>
        </label>
        <p style={styles.hint}>
          💡 You can find your quiz IDs on the course detail page after taking a quiz.
        </p>
      </div>

      {error && <div className="error-msg">{error}</div>}

      {/* Recommendation results */}
      {recommendation && (
        <>
          <section>
            <h2 style={styles.sectionTitle}>Performance Analysis</h2>
            <Recommendation data={recommendation} />
          </section>

          {/* AI Feedback */}
          <section>
            <div style={styles.feedbackHeader}>
              <h2 style={styles.sectionTitle}>AI Tutor Feedback</h2>
              <button
                className="btn btn-secondary"
                onClick={fetchAIFeedback}
                disabled={feedbackLoading}
              >
                {feedbackLoading ? "Generating…" : "🤖 Generate AI Feedback"}
              </button>
            </div>

            {feedbackLoading && (
              <div className="card" style={styles.feedbackCard}>
                <div style={styles.feedbackLoading}>
                  <div className="spinner" style={{ margin: "0 auto" }} />
                  <p style={{ color: "#64748b", fontSize: "0.875rem" }}>
                    The AI tutor is composing feedback…
                  </p>
                </div>
              </div>
            )}

            {feedback && !feedbackLoading && (
              <div className="card" style={styles.feedbackCard}>
                <div style={styles.feedbackMeta}>
                  <span style={styles.botIcon}>🤖</span>
                  <span style={styles.botLabel}>AI Tutor</span>
                </div>
                <p style={styles.feedbackText}>{feedback}</p>
              </div>
            )}
          </section>

          {/* Quick links */}
          <div style={styles.actions}>
            <button className="btn btn-outline" onClick={() => navigate("/courses")}>
              📚 Browse Courses
            </button>
            <button className="btn btn-secondary" onClick={() => navigate("/dashboard")}>
              🏠 Dashboard
            </button>
          </div>
        </>
      )}

      {/* Empty state */}
      {!recommendation && !loading && !error && (
        <div className="card" style={styles.emptyState}>
          <span style={{ fontSize: "3rem" }}>💡</span>
          <h3 style={{ fontWeight: 700, color: "#1e293b" }}>No recommendation yet</h3>
          <p style={{ color: "#64748b", fontSize: "0.875rem" }}>
            Enter a quiz ID above to see your personalised learning recommendation.
          </p>
          <button className="btn btn-primary" onClick={() => navigate("/courses")}>
            Take a Quiz →
          </button>
        </div>
      )}
    </main>
  );
}

const styles = {
  main: { maxWidth: 800, margin: "0 auto", padding: "2rem 1.25rem", display: "flex", flexDirection: "column", gap: "1.5rem" },
  inputCard: { display: "flex", flexDirection: "column", gap: "0.75rem" },
  label: { display: "flex", flexDirection: "column", gap: "0.4rem", fontWeight: 600, fontSize: "0.875rem", color: "#374151" },
  inputRow: { display: "flex", gap: "0.75rem" },
  input: {
    flex: 1,
    padding: "0.6rem 0.8rem",
    border: "1.5px solid #e2e8f0",
    borderRadius: "0.4rem",
    fontSize: "0.95rem",
    outline: "none",
  },
  hint: { fontSize: "0.8rem", color: "#94a3b8" },
  sectionTitle: { fontSize: "1.1rem", fontWeight: 700, color: "#1e293b", marginBottom: "0.75rem" },
  feedbackHeader: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.75rem", flexWrap: "wrap", gap: "0.5rem" },
  feedbackCard: { display: "flex", flexDirection: "column", gap: "0.75rem" },
  feedbackLoading: { display: "flex", flexDirection: "column", alignItems: "center", gap: "0.75rem", padding: "1rem 0" },
  feedbackMeta: { display: "flex", alignItems: "center", gap: "0.5rem" },
  botIcon: { fontSize: "1.5rem" },
  botLabel: { fontWeight: 700, fontSize: "0.875rem", color: "#4f46e5" },
  feedbackText: { fontSize: "0.9rem", color: "#374151", lineHeight: 1.8, whiteSpace: "pre-wrap" },
  actions: { display: "flex", gap: "0.75rem", flexWrap: "wrap" },
  emptyState: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "0.75rem",
    padding: "3rem",
    textAlign: "center",
  },
};
