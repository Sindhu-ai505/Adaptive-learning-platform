import React, { useState } from "react";
import { useAuth } from "../context/useAuth";

const LEVELS = ["beginner", "intermediate", "advanced"];
const STYLES = ["visual", "auditory", "reading", "kinesthetic"];

const styleInfo = {
  visual:      { icon: "👁️",  desc: "Learn best through diagrams, charts, and visual content" },
  auditory:    { icon: "🎧",  desc: "Learn best through listening, discussion, and explanations" },
  reading:     { icon: "📖",  desc: "Learn best through reading text and taking written notes" },
  kinesthetic: { icon: "🖐️", desc: "Learn best through practice, hands-on exercises, and doing" },
};

const levelInfo = {
  beginner:     { icon: "🌱", color: "#15803d", bg: "#dcfce7" },
  intermediate: { icon: "🌿", color: "#854d0e", bg: "#fef9c3" },
  advanced:     { icon: "🌳", color: "#1d4ed8", bg: "#dbeafe" },
};

export default function Profile() {
  const { user, updateProfile } = useAuth();

  const [form, setForm] = useState({
    name: user?.name || "",
    learning_level: user?.learning_level || "beginner",
    learning_style: user?.learning_style || "visual",
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  const isDirty =
    form.name !== user?.name ||
    form.learning_level !== user?.learning_level ||
    form.learning_style !== user?.learning_style;

  async function handleSave(e) {
    e.preventDefault();
    setError("");
    setSuccess(false);
    setLoading(true);
    try {
      await updateProfile({
        name: form.name,
        learning_level: form.learning_level,
        learning_style: form.learning_style,
      });
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to save changes.");
    } finally {
      setLoading(false);
    }
  }

  const lvl = levelInfo[form.learning_level] || levelInfo.beginner;

  return (
    <main style={styles.main}>
      {/* Header */}
      <div className="page-header">
        <h1>My Profile</h1>
        <p>Update your name, learning level and learning style</p>
      </div>

      <div style={styles.grid}>

        {/* ── Left: avatar card ── */}
        <div className="card" style={styles.avatarCard}>
          <div style={styles.avatarRing}>
            <div style={styles.avatar}>
              {form.name?.[0]?.toUpperCase() || "U"}
            </div>
          </div>
          <p style={styles.avatarName}>{form.name || user?.name}</p>
          <p style={styles.avatarEmail}>{user?.email}</p>

          <div style={{ ...styles.levelBadge, background: lvl.bg, color: lvl.color }}>
            {lvl.icon} {form.learning_level}
          </div>

          <div style={styles.stylePill}>
            {styleInfo[form.learning_style]?.icon} {form.learning_style} learner
          </div>
        </div>

        {/* ── Right: form ── */}
        <form onSubmit={handleSave} style={styles.form} noValidate>

          {/* Name */}
          <section className="card" style={styles.section}>
            <h2 style={styles.sectionTitle}>Personal Details</h2>
            <label style={styles.label}>
              Full name
              <input
                type="text"
                value={form.name}
                onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                style={styles.input}
                required
              />
            </label>
            <label style={styles.label}>
              Email address
              <input
                type="email"
                value={user?.email || ""}
                disabled
                style={{ ...styles.input, background: "#f8fafc", color: "#94a3b8", cursor: "not-allowed" }}
              />
              <span style={styles.hint}>Email cannot be changed</span>
            </label>
          </section>

          {/* Learning level */}
          <section className="card" style={styles.section}>
            <h2 style={styles.sectionTitle}>Learning Level</h2>
            <p style={styles.sectionDesc}>
              This affects which courses are highlighted and the difficulty of adaptive questions.
            </p>
            <div style={styles.optionGrid}>
              {LEVELS.map((lvlKey) => {
                const info = levelInfo[lvlKey];
                const selected = form.learning_level === lvlKey;
                return (
                  <button
                    key={lvlKey}
                    type="button"
                    onClick={() => setForm((f) => ({ ...f, learning_level: lvlKey }))}
                    style={{
                      ...styles.optionBtn,
                      borderColor: selected ? info.color : "#e2e8f0",
                      background: selected ? info.bg : "#fff",
                    }}
                    aria-pressed={selected}
                  >
                    <span style={styles.optionIcon}>{info.icon}</span>
                    <span style={{ ...styles.optionLabel, color: selected ? info.color : "#1e293b" }}>
                      {lvlKey.charAt(0).toUpperCase() + lvlKey.slice(1)}
                    </span>
                    {selected && <span style={{ ...styles.checkmark, color: info.color }}>✓</span>}
                  </button>
                );
              })}
            </div>
          </section>

          {/* Learning style */}
          <section className="card" style={styles.section}>
            <h2 style={styles.sectionTitle}>Learning Style</h2>
            <p style={styles.sectionDesc}>
              Choose how you prefer to absorb information. This personalises how content is presented.
            </p>
            <div style={styles.styleGrid}>
              {STYLES.map((styleKey) => {
                const info = styleInfo[styleKey];
                const selected = form.learning_style === styleKey;
                return (
                  <button
                    key={styleKey}
                    type="button"
                    onClick={() => setForm((f) => ({ ...f, learning_style: styleKey }))}
                    style={{
                      ...styles.styleBtn,
                      borderColor: selected ? "#4f46e5" : "#e2e8f0",
                      background: selected ? "#eef2ff" : "#fff",
                    }}
                    aria-pressed={selected}
                  >
                    <span style={styles.styleIcon}>{info.icon}</span>
                    <div style={styles.styleText}>
                      <p style={{ ...styles.styleName, color: selected ? "#4f46e5" : "#1e293b" }}>
                        {styleKey.charAt(0).toUpperCase() + styleKey.slice(1)}
                      </p>
                      <p style={styles.styleDesc}>{info.desc}</p>
                    </div>
                    {selected && <span style={{ ...styles.checkmark, color: "#4f46e5", marginLeft: "auto" }}>✓</span>}
                  </button>
                );
              })}
            </div>
          </section>

          {/* Feedback */}
          {error   && <div className="error-msg">{error}</div>}
          {success && <div className="success-msg">✓ Profile updated successfully!</div>}

          {/* Save button */}
          <button
            type="submit"
            className="btn btn-primary"
            style={styles.saveBtn}
            disabled={loading || !isDirty}
          >
            {loading ? "Saving…" : isDirty ? "Save Changes" : "No Changes"}
          </button>
        </form>
      </div>
    </main>
  );
}

const styles = {
  main: {
    maxWidth: 960,
    margin: "0 auto",
    padding: "2rem 1.25rem",
    display: "flex",
    flexDirection: "column",
    gap: "1.5rem",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "240px 1fr",
    gap: "1.5rem",
    alignItems: "start",
  },
  /* Avatar card */
  avatarCard: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "0.6rem",
    padding: "2rem 1rem",
    position: "sticky",
    top: 80,
    textAlign: "center",
  },
  avatarRing: {
    padding: 4,
    borderRadius: "50%",
    background: "linear-gradient(135deg, #4f46e5, #06b6d4)",
    marginBottom: "0.25rem",
  },
  avatar: {
    width: 72,
    height: 72,
    borderRadius: "50%",
    background: "#fff",
    border: "3px solid #fff",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "1.8rem",
    fontWeight: 800,
    color: "#4f46e5",
  },
  avatarName: { fontWeight: 700, fontSize: "1rem", color: "#1e293b" },
  avatarEmail: { fontSize: "0.78rem", color: "#94a3b8", wordBreak: "break-all" },
  levelBadge: {
    padding: "0.3rem 0.9rem",
    borderRadius: 99,
    fontSize: "0.78rem",
    fontWeight: 700,
    textTransform: "capitalize",
    marginTop: "0.25rem",
  },
  stylePill: {
    fontSize: "0.78rem",
    color: "#64748b",
    background: "#f1f5f9",
    borderRadius: 99,
    padding: "0.3rem 0.9rem",
    textTransform: "capitalize",
  },
  /* Form */
  form: { display: "flex", flexDirection: "column", gap: "1.25rem" },
  section: { display: "flex", flexDirection: "column", gap: "0.9rem" },
  sectionTitle: { fontSize: "1rem", fontWeight: 700, color: "#1e293b" },
  sectionDesc: { fontSize: "0.83rem", color: "#64748b", marginTop: "-0.4rem" },
  label: {
    display: "flex",
    flexDirection: "column",
    gap: "0.3rem",
    fontSize: "0.875rem",
    fontWeight: 600,
    color: "#374151",
  },
  input: {
    padding: "0.6rem 0.8rem",
    border: "1.5px solid #e2e8f0",
    borderRadius: "0.4rem",
    fontSize: "0.95rem",
    outline: "none",
    transition: "border-color 0.2s",
  },
  hint: { fontSize: "0.75rem", color: "#94a3b8", fontWeight: 400 },
  /* Level buttons */
  optionGrid: { display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: "0.75rem" },
  optionBtn: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "0.3rem",
    padding: "0.9rem 0.5rem",
    border: "2px solid",
    borderRadius: "0.5rem",
    background: "#fff",
    cursor: "pointer",
    transition: "all 0.15s",
    position: "relative",
  },
  optionIcon: { fontSize: "1.5rem" },
  optionLabel: { fontSize: "0.85rem", fontWeight: 700, textTransform: "capitalize" },
  checkmark: { fontSize: "0.85rem", fontWeight: 800, position: "absolute", top: 6, right: 8 },
  /* Style buttons */
  styleGrid: { display: "flex", flexDirection: "column", gap: "0.6rem" },
  styleBtn: {
    display: "flex",
    alignItems: "center",
    gap: "0.9rem",
    padding: "0.85rem 1rem",
    border: "2px solid",
    borderRadius: "0.5rem",
    background: "#fff",
    cursor: "pointer",
    textAlign: "left",
    transition: "all 0.15s",
  },
  styleIcon: { fontSize: "1.6rem", flexShrink: 0 },
  styleText: { display: "flex", flexDirection: "column", gap: "0.1rem" },
  styleName: { fontSize: "0.9rem", fontWeight: 700, textTransform: "capitalize" },
  styleDesc: { fontSize: "0.78rem", color: "#64748b" },
  /* Save */
  saveBtn: { padding: "0.75rem", fontSize: "1rem", width: "100%" },
};
