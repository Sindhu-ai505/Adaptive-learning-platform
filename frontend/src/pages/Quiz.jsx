import React, { useEffect, useState } from "react";
import { useParams, useLocation, useNavigate } from "react-router-dom";
import { quizzesApi, attemptsApi } from "../services/api";
import { useAuth } from "../context/useAuth";
import QuizQuestion from "../components/QuizQuestion";

export default function Quiz() {
  const { quizId } = useParams();
  const { state } = useLocation();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [quiz, setQuiz] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({}); // questionId → selected letter
  const [attemptId, setAttemptId] = useState(state?.attemptId || null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const { data } = await quizzesApi.get(quizId);
        setQuiz(data.quiz);
        setQuestions(data.questions || []);

        // Start attempt if not provided
        if (!state?.attemptId) {
          const { data: attempt } = await attemptsApi.start(user.id, quizId);
          setAttemptId(attempt.id);
        }
      } catch (err) {
        setError(err.response?.data?.detail || "Could not load quiz.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [quizId, user.id, state?.attemptId]);

  function selectAnswer(letter) {
    setAnswers((a) => ({ ...a, [questions[current].id]: letter }));
  }

  function next() {
    if (current < questions.length - 1) setCurrent((c) => c + 1);
  }

  function prev() {
    if (current > 0) setCurrent((c) => c - 1);
  }

  async function submit() {
    setSubmitting(true);
    try {
      // Submit each answer via the attempts API
      for (const q of questions) {
        const selected = answers[q.id];
        if (selected) {
          await attemptsApi.answer(attemptId, q.id, selected);
        }
      }
      navigate(`/results/${attemptId}`, { state: { quizId } });
    } catch (err) {
      setError(err.response?.data?.detail || "Could not submit quiz.");
      setSubmitting(false);
    }
  }

  if (loading) return <div style={styles.main}><div className="spinner" /></div>;
  if (error) return <div style={styles.main}><div className="error-msg">{error}</div></div>;
  if (!questions.length) return (
    <div style={styles.main}>
      <div className="card" style={{ textAlign: "center", color: "#64748b" }}>
        This quiz has no questions yet.
      </div>
    </div>
  );

  const q = questions[current];
  const answered = Object.keys(answers).length;
  const pct = Math.round((answered / questions.length) * 100);
  const isLast = current === questions.length - 1;

  return (
    <main style={styles.main}>
      {/* Header */}
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>{quiz?.title}</h1>
          <p style={styles.sub}>{answered} of {questions.length} answered</p>
        </div>
        <div style={styles.progress}>
          <div style={styles.progressBar}>
            <div style={{ ...styles.progressFill, width: `${pct}%` }} />
          </div>
          <span style={styles.progressPct}>{pct}%</span>
        </div>
      </div>

      {/* Question dots */}
      <div style={styles.dots}>
        {questions.map((qn, i) => (
          <button
            key={qn.id}
            onClick={() => setCurrent(i)}
            aria-label={`Go to question ${i + 1}`}
            style={{
              ...styles.dot,
              ...(i === current ? styles.dotActive : {}),
              ...(answers[qn.id] ? styles.dotAnswered : {}),
            }}
          />
        ))}
      </div>

      {/* Question card */}
      <div className="card" style={styles.questionCard}>
        <QuizQuestion
          question={q}
          questionNumber={current + 1}
          totalQuestions={questions.length}
          selectedAnswer={answers[q.id] || null}
          onSelect={selectAnswer}
          disabled={submitting}
        />
      </div>

      {/* Navigation */}
      <div style={styles.nav}>
        <button className="btn btn-outline" onClick={prev} disabled={current === 0 || submitting}>
          ← Previous
        </button>

        {!isLast ? (
          <button className="btn btn-primary" onClick={next} disabled={submitting}>
            Next →
          </button>
        ) : (
          <button
            className="btn btn-primary"
            onClick={submit}
            disabled={submitting || answered === 0}
            style={{ background: "#22c55e", minWidth: 140 }}
          >
            {submitting ? "Submitting…" : "Submit Quiz ✓"}
          </button>
        )}
      </div>

      {error && <div className="error-msg">{error}</div>}
    </main>
  );
}

const styles = {
  main: { maxWidth: 750, margin: "0 auto", padding: "2rem 1.25rem", display: "flex", flexDirection: "column", gap: "1.25rem" },
  header: { display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "1rem" },
  title: { fontSize: "1.4rem", fontWeight: 800, color: "#1e293b" },
  sub: { fontSize: "0.85rem", color: "#64748b", marginTop: "0.2rem" },
  progress: { display: "flex", alignItems: "center", gap: "0.75rem", minWidth: 180 },
  progressBar: { flex: 1, height: 8, background: "#e2e8f0", borderRadius: 99, overflow: "hidden" },
  progressFill: { height: "100%", background: "#4f46e5", borderRadius: 99, transition: "width 0.4s" },
  progressPct: { fontSize: "0.8rem", fontWeight: 700, color: "#4f46e5", minWidth: 30 },
  dots: { display: "flex", gap: "0.4rem", flexWrap: "wrap" },
  dot: {
    width: 12, height: 12,
    borderRadius: "50%",
    border: "1.5px solid #cbd5e1",
    background: "#f8fafc",
    cursor: "pointer",
    padding: 0,
    transition: "background 0.2s",
  },
  dotActive: { border: "1.5px solid #4f46e5", background: "#4f46e5" },
  dotAnswered: { border: "1.5px solid #22c55e", background: "#22c55e" },
  questionCard: { padding: "2rem" },
  nav: { display: "flex", justifyContent: "space-between", alignItems: "center" },
};
