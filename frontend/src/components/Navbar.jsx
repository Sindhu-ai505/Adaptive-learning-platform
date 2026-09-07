import React, { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/useAuth";

export default function Navbar() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  const links = [
    { to: "/dashboard", label: "Dashboard" },
    { to: "/courses", label: "Courses" },
    { to: "/recommendations", label: "Recommendations" },
  ];

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <nav style={styles.nav}>
      <div style={styles.inner}>
        {/* Logo */}
        <Link to="/dashboard" style={styles.logo}>
          🎓 AdaptiveLearn
        </Link>

        {/* Desktop links */}
        <div style={styles.links}>
          {links.map((l) => (
            <Link
              key={l.to}
              to={l.to}
              style={{
                ...styles.link,
                ...(location.pathname.startsWith(l.to) ? styles.linkActive : {}),
              }}
            >
              {l.label}
            </Link>
          ))}
        </div>

        {/* User info + logout */}
        <div style={styles.right}>
          <Link
            to="/profile"
            style={{
              display: "flex",
              alignItems: "center",
              gap: "0.4rem",
              padding: "0.25rem 0.6rem",
              borderRadius: "0.4rem",
              background: location.pathname === "/profile" ? "#eef2ff" : "transparent",
              textDecoration: "none",
              transition: "background 0.15s",
            }}
            title="Edit profile"
          >
            <span style={{
              width: 28, height: 28, borderRadius: "50%",
              background: "#4f46e5", color: "#fff",
              display: "inline-flex", alignItems: "center", justifyContent: "center",
              fontWeight: 700, fontSize: "0.8rem", flexShrink: 0,
            }}>
              {user?.name?.[0]?.toUpperCase() || "U"}
            </span>
            <span style={{ fontSize: "0.875rem", fontWeight: 500, color: location.pathname === "/profile" ? "#4f46e5" : "#475569" }}>
              {user?.name}
            </span>
          </Link>
          <button onClick={handleLogout} className="btn btn-outline" style={{ fontSize: "0.8rem" }}>
            Logout
          </button>
        </div>

        {/* Mobile hamburger */}
        <button style={styles.hamburger} onClick={() => setMenuOpen((o) => !o)} aria-label="Toggle menu">
          ☰
        </button>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <div style={styles.mobileMenu}>
          {links.map((l) => (
            <Link
              key={l.to}
              to={l.to}
              style={styles.mobileLink}
              onClick={() => setMenuOpen(false)}
            >
              {l.label}
            </Link>
          ))}
          <button onClick={handleLogout} style={styles.mobileLogout}>
            Logout
          </button>
        </div>
      )}
    </nav>
  );
}

const styles = {
  nav: {
    background: "#fff",
    borderBottom: "1px solid #e2e8f0",
    position: "sticky",
    top: 0,
    zIndex: 100,
    boxShadow: "0 1px 3px rgba(0,0,0,.08)",
  },
  inner: {
    maxWidth: 1100,
    margin: "0 auto",
    padding: "0 1.25rem",
    height: 60,
    display: "flex",
    alignItems: "center",
    gap: "1.5rem",
  },
  logo: {
    fontSize: "1.15rem",
    fontWeight: 700,
    color: "#4f46e5",
    textDecoration: "none",
    whiteSpace: "nowrap",
  },
  links: {
    display: "flex",
    gap: "1.25rem",
    flex: 1,
  },
  link: {
    fontSize: "0.9rem",
    fontWeight: 500,
    color: "#64748b",
    textDecoration: "none",
    padding: "0.2rem 0",
    borderBottom: "2px solid transparent",
  },
  linkActive: {
    color: "#4f46e5",
    borderBottom: "2px solid #4f46e5",
  },
  right: {
    display: "flex",
    alignItems: "center",
    gap: "1rem",
    whiteSpace: "nowrap",
  },
  userName: {
    fontSize: "0.875rem",
    color: "#475569",
  },
  hamburger: {
    display: "none",
    background: "none",
    border: "none",
    fontSize: "1.4rem",
    cursor: "pointer",
  },
  mobileMenu: {
    display: "flex",
    flexDirection: "column",
    padding: "0.75rem 1.25rem 1rem",
    gap: "0.5rem",
    borderTop: "1px solid #e2e8f0",
  },
  mobileLink: {
    padding: "0.5rem 0",
    color: "#1e293b",
    fontWeight: 500,
    textDecoration: "none",
  },
  mobileLogout: {
    background: "none",
    border: "none",
    color: "#ef4444",
    fontWeight: 600,
    textAlign: "left",
    padding: "0.5rem 0",
    cursor: "pointer",
  },
};
