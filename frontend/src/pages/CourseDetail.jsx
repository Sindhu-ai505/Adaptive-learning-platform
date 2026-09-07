import React, { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { coursesApi, quizzesApi, attemptsApi } from "../services/api";
import { useAuth } from "../context/AuthContext";
import LessonContent from "../components/LessonContent";

const diffMap = {
  beginner: "badge-green", intermediate: "badge-yellow", advanced: "badge-red",
  easy: "badge-green", medium: "badge-yellow", hard: "badge-red",
};

const styleInfo = {
  visual:      { icon: "👁️",  label: "Visual",      color: "#4f46e5", bg: "#eef2ff" },
  auditory:    { icon: "🎧",  label: "Auditory",    color: "#0e7490", bg: "#ecfeff" },
  reading:     { icon: "📖",  label: "Reading",     color: "#6d28d9", bg: "#ede9fe" },
  kinesthetic: { icon: "🖐️", label: "Kinesthetic", color: "#15803d", bg: "#dcfce7" },
};

export default function CourseDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [course, setCourse]           = useState(null);
  const [lessons, setLessons]         = useState([]);
  const [loading, setLoading]         = useState(true);
  const [error, setError]             = useState("");
  const [expandedLesson, setExpanded] = useState(null);
  const [quizData, setQuizData]       = useState({});
  const [quizLoading, setQuizLoading] = useState({});

  const styleKey = user?.learning_style || "visual";
  const style    = styleInfo[styleKey] || styleInfo.visual;

  useEffect(() => {
    coursesApi.get(id)
      .then(({ data }) => { setCourse(data.course); setLessons(data.lessons || []); })
      .catch(() => setError("Could not load course."))
      .finally(() => setLoading(false));
  }, [id]);

  async function toggleLesson(lessonId) {
    if (expandedLesson === lessonId) {
      setExpanded(null);
      return;
    }
    setExpanded(lessonId);
    // Auto-fetch the quiz for this lesson when it opens
    if (quizData[lessonId] === undefined) {
      loadQuiz(lessonId);
    }
  }

  async function loadQuiz(lessonId) {
    if (quizData[lessonId]) return;
    setQuizLoading((l) => ({ ...l, [lessonId]: true }));
    try {
      // Always look up by lesson_id — guaranteed to fetch the right quiz
      const { data } = await quizzesApi.byLesson(lessonId);
      setQuizData((d) => ({ ...d, [lessonId]: data }));
    } catch {
      // No quiz for this lesson
      setQuizData((d) => ({ ...d, [lessonId]: null }));
    } finally {
      setQuizLoading((l) => ({ ...l, [lessonId]: false }));
    }
  }

  async function startQuiz(quizId) {
    try {
      const { data } = await attemptsApi.start(user.id, quizId);
      navigate(`/quiz/${quizId}`, { state: { attemptId: data.id } });
    } catch (err) {
      alert(err.response?.data?.detail || "Could not start quiz.");
    }
  }

  if (loading) return <div style={S.main}><div className="spinner" /></div>;
  if (error)   return <div style={S.main}><div className="error-msg">{error}</div></div>;

  return (
    <main style={S.main}>
      <button onClick={() => navigate("/courses")} style={S.back}>← Back to Courses</button>

      {/* Course header */}
      <div style={S.header} className="card">
        <div style={S.headerLeft}>
          <span style={S.bigIcon}>📚</span>
          <div>
            <div style={S.meta}>
              {course.category && <span className="badge badge-purple">{course.category}</span>}
              <span className={`badge ${diffMap[course.difficulty] || "badge-blue"}`}>{course.difficulty}</span>
            </div>
            <h1 style={S.title}>{course.title}</h1>
            {course.description && <p style={S.desc}>{course.description}</p>}
          </div>
        </div>
        <div style={S.statsRow}>
          <div style={S.stat}>
            <span style={S.statNum}>{lessons.length}</span>
            <span style={S.statLabel}>Lessons</span>
          </div>
        </div>
      </div>

      {/* Learning style banner */}
      <div style={{ ...S.styleBanner, background: style.bg, borderColor: style.color + "44" }}>
        <span style={S.styleIcon}>{style.icon}</span>
        <div style={{ flex: 1 }}>
          <p style={{ ...S.styleTitle, color: style.color }}>
            {style.label} Learning Mode active
          </p>
          <p style={S.styleHint}>
            {styleKey === "visual"      && "Lesson content is shown as colour-coded visual cards."}
            {styleKey === "auditory"    && "Press ▶ Play inside any lesson to hear it read aloud."}
            {styleKey === "reading"     && "Lessons are formatted for focused reading with a summary and glossary."}
            {styleKey === "kinesthetic" && "Lessons include fill-in-the-blank exercises to learn by doing."}
          </p>
        </div>
        <Link to="/profile" style={{ ...S.changeStyle, color: style.color }}>
          Change style →
        </Link>
      </div>

      {/* Lessons */}
      <section>
        <h2 style={S.sectionTitle}>Lessons</h2>

        {lessons.length === 0 && (
          <div className="card" style={{ color: "#64748b", textAlign: "center" }}>
            No lessons available yet.
          </div>
        )}

        <div style={S.lessonList}>
          {lessons.map((lesson, idx) => (
            <div key={lesson.id} className="card" style={S.lessonCard}>
              {/* Toggle bar */}
              <button
                style={S.toggle}
                onClick={() => toggleLesson(lesson.id)}
                aria-expanded={expandedLesson === lesson.id}
              >
                <span style={S.lessonNum}>{idx + 1}</span>
                <span style={S.lessonTitle}>{lesson.title}</span>
                <span className={`badge ${diffMap[lesson.difficulty] || "badge-blue"}`}>
                  {lesson.difficulty}
                </span>
                <span style={S.chevron}>{expandedLesson === lesson.id ? "▲" : "▼"}</span>
              </button>

              {/* Expanded body */}
              {expandedLesson === lesson.id && (
                <div style={S.lessonBody}>
                  {/* Adaptive content renderer */}
                  <LessonContent content={lesson.content} lessonTitle={lesson.title} />

                  {/* Quiz */}
                  <div style={S.quizSection}>
                    <LessonQuiz
                      lessonId={lesson.id}
                      quizData={quizData}
                      quizLoading={quizLoading}
                      onLoadQuiz={loadQuiz}
                      onStartQuiz={startQuiz}
                    />
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}

function LessonQuiz({ lessonId, quizData, quizLoading, onLoadQuiz, onStartQuiz }) {
  // quizData is keyed by lessonId; the value contains the real quiz object
  const entry   = quizData[lessonId];
  const loading = quizLoading[lessonId];

  // Not fetched yet
  if (entry === undefined && !loading) {
    return (
      <button className="btn btn-secondary" style={{ fontSize: "0.85rem" }}
        onClick={() => onLoadQuiz(lessonId)}>
        📝 Check for Quiz
      </button>
    );
  }

  if (loading) return <span style={{ fontSize: "0.85rem", color: "#64748b" }}>Loading quiz…</span>;

  // Fetched but no quiz exists for this lesson
  if (!entry || !entry.questions?.length) {
    return <span style={{ fontSize: "0.85rem", color: "#94a3b8" }}>No quiz for this lesson.</span>;
  }

  // Use the real quiz ID from the API response
  const realQuizId = entry.quiz.id;

  return (
    <div style={{ display: "flex", alignItems: "center", gap: "1rem", flexWrap: "wrap" }}>
      <span style={{ fontSize: "0.875rem", color: "#475569" }}>
        📝 <strong>{entry.quiz.title}</strong> — {entry.questions.length} questions
      </span>
      <button className="btn btn-primary" style={{ fontSize: "0.85rem" }}
        onClick={() => onStartQuiz(realQuizId)}>
        Start Quiz →
      </button>
    </div>
  );
}

const S = {
  main: { maxWidth: 900, margin: "0 auto", padding: "2rem 1.25rem", display: "flex", flexDirection: "column", gap: "1.5rem" },
  back: { background: "none", border: "none", color: "#4f46e5", fontWeight: 600, fontSize: "0.875rem", cursor: "pointer", textAlign: "left", padding: 0 },
  header: { display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "1rem", flexWrap: "wrap" },
  headerLeft: { display: "flex", gap: "1rem", alignItems: "flex-start" },
  bigIcon: { fontSize: "3rem", flexShrink: 0 },
  meta: { display: "flex", gap: "0.5rem", marginBottom: "0.4rem", flexWrap: "wrap" },
  title: { fontSize: "1.5rem", fontWeight: 800, color: "#1e293b" },
  desc: { color: "#64748b", fontSize: "0.9rem", marginTop: "0.25rem", maxWidth: 500 },
  statsRow: { display: "flex", gap: "0.75rem" },
  stat: { textAlign: "center", background: "#f8fafc", borderRadius: "0.5rem", padding: "0.75rem 1.5rem" },
  statNum: { display: "block", fontSize: "2rem", fontWeight: 800, color: "#4f46e5" },
  statLabel: { fontSize: "0.75rem", color: "#64748b", textTransform: "uppercase", fontWeight: 600 },
  /* Style banner */
  styleBanner: {
    display: "flex", alignItems: "flex-start", gap: "0.75rem",
    border: "1.5px solid", borderRadius: "0.5rem", padding: "0.85rem 1rem",
  },
  styleIcon: { fontSize: "1.6rem", flexShrink: 0, marginTop: "0.1rem" },
  styleTitle: { fontWeight: 700, fontSize: "0.875rem", margin: 0 },
  styleHint: { fontSize: "0.8rem", color: "#64748b", margin: "0.15rem 0 0" },
  changeStyle: { fontSize: "0.78rem", fontWeight: 700, whiteSpace: "nowrap", textDecoration: "none", marginTop: "0.2rem" },
  /* Lessons */
  sectionTitle: { fontSize: "1.15rem", fontWeight: 700, color: "#1e293b", marginBottom: "0.75rem" },
  lessonList: { display: "flex", flexDirection: "column", gap: "0.75rem" },
  lessonCard: { padding: 0 },
  toggle: {
    display: "flex", alignItems: "center", gap: "0.75rem",
    width: "100%", background: "none", border: "none",
    padding: "1rem 1.5rem", cursor: "pointer", textAlign: "left",
  },
  lessonNum: {
    display: "inline-flex", alignItems: "center", justifyContent: "center",
    width: 28, height: 28, borderRadius: "50%",
    background: "#eef2ff", color: "#4f46e5", fontWeight: 700, fontSize: "0.8rem", flexShrink: 0,
  },
  lessonTitle: { flex: 1, fontWeight: 600, color: "#1e293b", fontSize: "0.95rem" },
  chevron: { color: "#94a3b8", fontSize: "0.75rem", flexShrink: 0 },
  lessonBody: {
    padding: "0 1.5rem 1.5rem",
    borderTop: "1px solid #f1f5f9",
    display: "flex", flexDirection: "column", gap: "1.25rem",
  },
  quizSection: { borderTop: "1px dashed #e2e8f0", paddingTop: "1rem" },
};
