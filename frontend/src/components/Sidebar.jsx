import React from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const navItems = [
  { to: "/dashboard", icon: "🏠", label: "Dashboard" },
  { to: "/courses", icon: "📚", label: "Courses" },
  { to: "/recommendations", icon: "💡", label: "Recommendations" },
];

export default function Sidebar() {
  const { pathname } = useLocation();
  const { user } = useAuth();

  return (
    <aside style={styles.sidebar} aria-label="Sidebar navigation">
      <div style={styles.profile}>
        <div style={styles.avatar}>{user?.name?.[0]?.toUpperCase() || "U"}</div>
        <div>
          <p style={styles.name}>{user?.name}</p>
          <p style={styles.level}>{user?.learning_level}</p>
        </div>
      </div>

      <nav>
        {navItems.map((item) => (
          <Link
            key={item.to}
            to={item.to}
            style={{
              ...styles.item,
              ...(pathname.startsWith(item.to) ? styles.itemActive : {}),
            }}
          >
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>
    </aside>
  );
}

const styles = {
  sidebar: {
    width: 220,
    background: "#fff",
    borderRight: "1px solid #e2e8f0",
    padding: "1.5rem 1rem",
    display: "flex",
    flexDirection: "column",
    gap: "1.5rem",
    minHeight: "calc(100vh - 60px)",
  },
  profile: {
    display: "flex",
    alignItems: "center",
    gap: "0.75rem",
    padding: "0.75rem",
    background: "#f8fafc",
    borderRadius: "0.5rem",
  },
  avatar: {
    width: 38,
    height: 38,
    borderRadius: "50%",
    background: "#4f46e5",
    color: "#fff",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: 700,
    fontSize: "1.1rem",
    flexShrink: 0,
  },
  name: { fontWeight: 600, fontSize: "0.875rem", color: "#1e293b" },
  level: { fontSize: "0.75rem", color: "#64748b", textTransform: "capitalize" },
  item: {
    display: "flex",
    alignItems: "center",
    gap: "0.6rem",
    padding: "0.65rem 0.75rem",
    borderRadius: "0.4rem",
    color: "#475569",
    fontSize: "0.9rem",
    fontWeight: 500,
    textDecoration: "none",
    marginBottom: "0.15rem",
    transition: "background 0.15s",
  },
  itemActive: {
    background: "#eef2ff",
    color: "#4f46e5",
    fontWeight: 700,
  },
};
