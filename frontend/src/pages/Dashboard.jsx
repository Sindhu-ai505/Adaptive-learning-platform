import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { coursesApi } from "../services/api";
import CourseCard from "../components/CourseCard";

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    coursesApi
      .list()
      .then(({ data }) => setCourses(data.slice(0, 6)))
      .catch(() => setError("Could not load courses."))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main style={styles.main}>
      {/* Hero */}
      <section style={styles.hero}>
        <div>
          <h1 style={styles.heroTitle}>
            Welcome back, {user?.name?.split(" ")[0]} 👋
          </h1>
          <p style={styles.heroSub}>
            You&apos;re a <strong>{user?.learning_level}</strong> learner. Keep going!
          </p>
        </div>
        <div style={styles.heroStats}>
          <StatChip icon="📖" label="Level" value={user?.learning_level} color="#4f46e5" />
          <StatChip icon="🎨" label="Style" value={user?.learning_style} color="#06b6d4" />
        </div>
      </section>

      {/* Quick actions */}
      <section>
        <h2 style={styles.sectionTitle}>Quick Actions</h2>
        <div style={styles.actions}>
          <ActionCard
            icon="📚"
            title="Browse Courses"
            desc="Explore all available courses"
            onClick={() => navigate("/courses")}
            color="#4f46e5"
          />
          <ActionCard
            icon="💡"
            title="My Recommendations"
            desc="See personalised suggestions"
            onClick={() => navigate("/recommendations")}
            color="#06b6d4"
          />
        </div>
      </section>

      {/* Featured courses */}
      <section>
        <div style={styles.sectionHeader}>
          <h2 style={styles.sectionTitle}>Featured Courses</h2>
          <button className="btn btn-secondary" onClick={() => navigate("/courses")}>
            View all →
          </button>
        </div>

        {loading && <div className="spinner" />}
        {error && <div className="error-msg">{error}</div>}

        {!loading && !error && courses.length === 0 && (
          <div className="card" style={{ textAlign: "center", color: "#64748b" }}>
            No courses yet.{" "}
            <button className="btn btn-primary" style={{ marginLeft: 8 }} onClick={() => navigate("/courses")}>
              Add your first course
            </button>
          </div>
        )}

        {!loading && courses.length > 0 && (
          <div className="grid-2">
            {courses.map((c) => (
              <CourseCard key={c.id} course={c} />
            ))}
          </div>
        )}
      </section>
    </main>
  );
}

function StatChip({ icon, label, value, color }) {
  return (
    <div style={{ ...chipStyles.chip, borderColor: color + "33" }}>
      <span style={chipStyles.icon}>{icon}</span>
      <div>
        <p style={chipStyles.label}>{label}</p>
        <p style={{ ...chipStyles.value, color }}>{value}</p>
      </div>
    </div>
  );
}

function ActionCard({ icon, title, desc, onClick, color }) {
  return (
    <button onClick={onClick} style={{ ...actionStyles.card, borderTopColor: color }} className="card">
      <span style={actionStyles.icon}>{icon}</span>
      <div>
        <p style={actionStyles.title}>{title}</p>
        <p style={actionStyles.desc}>{desc}</p>
      </div>
    </button>
  );
}

const styles = {
  main: {
    maxWidth: 1100,
    margin: "0 auto",
    padding: "2rem 1.25rem",
    display: "flex",
    flexDirection: "column",
    gap: "2rem",
  },
  hero: {
    background: "linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)",
    borderRadius: "0.75rem",
    padding: "2rem",
    color: "#fff",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    flexWrap: "wrap",
    gap: "1rem",
  },
  heroTitle: { fontSize: "1.75rem", fontWeight: 800 },
  heroSub: { fontSize: "1rem", opacity: 0.85, marginTop: "0.25rem" },
  heroStats: { display: "flex", gap: "0.75rem", flexWrap: "wrap" },
  sectionTitle: { fontSize: "1.2rem", fontWeight: 700, color: "#1e293b" },
  sectionHeader: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" },
  actions: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))", gap: "1rem", marginTop: "0.75rem" },
};

const chipStyles = {
  chip: {
    display: "flex",
    alignItems: "center",
    gap: "0.6rem",
    background: "rgba(255,255,255,0.15)",
    border: "1px solid rgba(255,255,255,0.3)",
    borderRadius: "0.5rem",
    padding: "0.6rem 0.9rem",
  },
  icon: { fontSize: "1.4rem" },
  label: { fontSize: "0.7rem", opacity: 0.75, textTransform: "uppercase", fontWeight: 600 },
  value: { fontSize: "0.9rem", fontWeight: 700, textTransform: "capitalize", color: "#fff" },
};

const actionStyles = {
  card: {
    display: "flex",
    alignItems: "center",
    gap: "1rem",
    border: "1px solid #e2e8f0",
    borderTop: "3px solid",
    background: "#fff",
    borderRadius: "0.5rem",
    padding: "1.25rem",
    cursor: "pointer",
    textAlign: "left",
    boxShadow: "0 1px 3px rgba(0,0,0,.08)",
    transition: "box-shadow 0.2s",
  },
  icon: { fontSize: "2rem" },
  title: { fontWeight: 700, color: "#1e293b", fontSize: "0.95rem" },
  desc: { fontSize: "0.8rem", color: "#64748b", marginTop: "0.15rem" },
};
