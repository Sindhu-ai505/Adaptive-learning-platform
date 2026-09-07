import React, { useEffect, useState } from "react";
import { coursesApi } from "../services/api";
import CourseCard from "../components/CourseCard";

const DIFFICULTIES = ["all", "beginner", "intermediate", "advanced"];

export default function Courses() {
  const [courses, setCourses] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [difficulty, setDifficulty] = useState("all");

  useEffect(() => {
    coursesApi
      .list()
      .then(({ data }) => {
        setCourses(data);
        setFiltered(data);
      })
      .catch(() => setError("Could not load courses."))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    let result = courses;
    if (difficulty !== "all") {
      result = result.filter((c) => c.difficulty?.toLowerCase() === difficulty);
    }
    if (search.trim()) {
      const q = search.toLowerCase();
      result = result.filter(
        (c) =>
          c.title?.toLowerCase().includes(q) ||
          c.description?.toLowerCase().includes(q) ||
          c.category?.toLowerCase().includes(q)
      );
    }
    setFiltered(result);
  }, [search, difficulty, courses]);

  return (
    <main style={styles.main}>
      <div className="page-header">
        <h1>Courses</h1>
        <p>Browse and explore all available courses</p>
      </div>

      {/* Filter bar */}
      <div style={styles.filterBar}>
        <input
          type="search"
          placeholder="Search courses…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={styles.searchInput}
          aria-label="Search courses"
        />
        <div style={styles.pills}>
          {DIFFICULTIES.map((d) => (
            <button
              key={d}
              onClick={() => setDifficulty(d)}
              className={`btn ${difficulty === d ? "btn-primary" : "btn-outline"}`}
              style={styles.pill}
            >
              {d.charAt(0).toUpperCase() + d.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {loading && <div className="spinner" />}
      {error && <div className="error-msg">{error}</div>}

      {!loading && filtered.length === 0 && (
        <div className="card" style={{ textAlign: "center", color: "#64748b", padding: "3rem" }}>
          No courses match your search.
        </div>
      )}

      {!loading && filtered.length > 0 && (
        <>
          <p style={styles.count}>{filtered.length} course{filtered.length !== 1 ? "s" : ""} found</p>
          <div className="grid-2">
            {filtered.map((c) => (
              <CourseCard key={c.id} course={c} />
            ))}
          </div>
        </>
      )}
    </main>
  );
}

const styles = {
  main: { maxWidth: 1100, margin: "0 auto", padding: "2rem 1.25rem", display: "flex", flexDirection: "column", gap: "1.5rem" },
  filterBar: { display: "flex", gap: "0.75rem", flexWrap: "wrap", alignItems: "center" },
  searchInput: {
    flex: 1,
    minWidth: 200,
    padding: "0.55rem 0.9rem",
    border: "1.5px solid #e2e8f0",
    borderRadius: "0.4rem",
    fontSize: "0.9rem",
    outline: "none",
  },
  pills: { display: "flex", gap: "0.4rem", flexWrap: "wrap" },
  pill: { padding: "0.4rem 0.85rem", fontSize: "0.8rem" },
  count: { fontSize: "0.85rem", color: "#64748b" },
};
