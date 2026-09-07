import React from "react";
import { useNavigate } from "react-router-dom";

const difficultyBadge = {
  beginner: "badge-green",
  intermediate: "badge-yellow",
  advanced: "badge-red",
  medium: "badge-yellow",
  hard: "badge-red",
  easy: "badge-green",
};

export default function CourseCard({ course }) {
  const navigate = useNavigate();
  const badgeClass = difficultyBadge[course.difficulty?.toLowerCase()] || "badge-blue";

  return (
    <div
      className="card"
      style={styles.card}
      onClick={() => navigate(`/courses/${course.id}`)}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === "Enter" && navigate(`/courses/${course.id}`)}
      aria-label={`View course: ${course.title}`}
    >
      <div style={styles.iconRow}>
        <span style={styles.icon}>📚</span>
        {course.category && (
          <span className="badge badge-purple">{course.category}</span>
        )}
      </div>
      <h3 style={styles.title}>{course.title}</h3>
      {course.description && (
        <p style={styles.desc}>{course.description}</p>
      )}
      <div style={styles.footer}>
        <span className={`badge ${badgeClass}`}>{course.difficulty}</span>
        <span style={styles.arrow}>View →</span>
      </div>
    </div>
  );
}

const styles = {
  card: {
    cursor: "pointer",
    transition: "box-shadow 0.2s, transform 0.15s",
    display: "flex",
    flexDirection: "column",
    gap: "0.6rem",
  },
  iconRow: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
  icon: { fontSize: "1.75rem" },
  title: { fontSize: "1.05rem", fontWeight: 700, color: "#1e293b" },
  desc: {
    fontSize: "0.85rem",
    color: "#64748b",
    display: "-webkit-box",
    WebkitLineClamp: 2,
    WebkitBoxOrient: "vertical",
    overflow: "hidden",
  },
  footer: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: "auto",
  },
  arrow: { fontSize: "0.85rem", color: "#4f46e5", fontWeight: 600 },
};
