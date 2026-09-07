/**
 * LessonContent — renders lesson text differently based on the user's learning style.
 *
 * visual      → structured cards with colour-coded sections and key-term highlights
 * auditory    → text-to-speech player with speed/voice controls
 * reading     → clean typography-focused layout with a summary and glossary
 * kinesthetic → interactive "reveal & check" exercise where the user fills blanks
 */

import React, { useState, useEffect, useRef, useCallback } from "react";
import { useAuth } from "../context/useAuth";

// ─── helpers ────────────────────────────────────────────────────────────────

/** Split lesson text into logical sections (separated by blank lines or bullet groups) */
function parseSections(text) {
  if (!text) return [];
  // Split on double newline or a line that ends with a colon (sub-heading)
  const raw = text.split(/\n\n+/);
  return raw.map((block) => {
    const lines = block.trim().split("\n");
    const heading = lines[0].endsWith(":") ? lines[0].slice(0, -1) : null;
    const body = heading ? lines.slice(1).join("\n") : lines.join("\n");
    return { heading, body };
  }).filter((s) => s.body.trim());
}

/** Extract bullet points from a body string */
function parseBullets(body) {
  return body.split("\n").map((l) => l.replace(/^[•\-\*]\s*/, "").trim()).filter(Boolean);
}

/** Bold any word/phrase after "—" or preceded by "•" on its own line */
function highlightKeyTerms(text) {
  // Highlight text between backticks or after bullet dashes
  return text.replace(/`([^`]+)`/g, "<strong>$1</strong>");
}

/** Pull out all capitalised proper-noun-like terms as a mini glossary */
function extractKeyTerms(text) {
  const matches = [...text.matchAll(/\b([A-Z][a-zA-Z]{2,}(?:\s[A-Z][a-zA-Z]+)*)\b/g)];
  const unique = [...new Set(matches.map((m) => m[1]))].filter(
    (t) => !["What", "Which", "How", "When", "Where", "This", "These", "The", "In", "At", "For"].includes(t)
  );
  return unique.slice(0, 12);
}

/** Create a fill-in-the-blank exercise from key sentences */
function buildExercises(text) {
  const sentences = text
    .split(/[.!\n]/)
    .map((s) => s.trim())
    .filter((s) => s.length > 40 && s.length < 200);

  // Pick up to 5 sentences and blank out a key word (≥5 chars)
  const exercises = [];
  for (const sentence of sentences) {
    if (exercises.length >= 5) break;
    const words = sentence.split(" ").filter((w) => w.replace(/[^a-zA-Z]/g, "").length >= 5);
    if (!words.length) continue;
    // pick the longest word as the "key" answer
    const answer = words.sort((a, b) => b.length - a.length)[0].replace(/[^a-zA-Z]/g, "");
    const blank = sentence.replace(new RegExp(answer, "i"), "________");
    if (blank !== sentence) exercises.push({ sentence: blank, answer: answer.toLowerCase(), original: sentence });
  }
  return exercises;
}

// ─── Section colour palette (cycles) ────────────────────────────────────────
const SECTION_COLORS = [
  { border: "#4f46e5", bg: "#eef2ff", head: "#3730a3" },
  { border: "#06b6d4", bg: "#ecfeff", head: "#0e7490" },
  { border: "#22c55e", bg: "#dcfce7", head: "#15803d" },
  { border: "#f59e0b", bg: "#fef9c3", head: "#92400e" },
  { border: "#ec4899", bg: "#fce7f3", head: "#9d174d" },
];

// ════════════════════════════════════════════════════════════════════════════
// VISUAL STYLE
// ════════════════════════════════════════════════════════════════════════════
function VisualContent({ content }) {
  const sections = parseSections(content);
  const keyTerms = extractKeyTerms(content);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      <StyleBanner icon="👁️" label="Visual Mode" color="#4f46e5" bg="#eef2ff"
        desc="Content is structured into visual sections with highlighted key concepts." />

      {/* Key terms strip */}
      {keyTerms.length > 0 && (
        <div style={vStyles.termStrip}>
          <span style={vStyles.termLabel}>🔑 Key Terms:</span>
          {keyTerms.map((t) => (
            <span key={t} style={vStyles.term}>{t}</span>
          ))}
        </div>
      )}

      {/* Colour-coded section cards */}
      {sections.map((sec, i) => {
        const col = SECTION_COLORS[i % SECTION_COLORS.length];
        const bullets = sec.body.includes("\n") ? parseBullets(sec.body) : null;
        return (
          <div key={i} style={{ ...vStyles.card, borderLeftColor: col.border, background: col.bg }}>
            {sec.heading && (
              <p style={{ ...vStyles.cardHead, color: col.head }}>
                {sectionIcon(i)} {sec.heading}
              </p>
            )}
            {bullets ? (
              <ul style={vStyles.ul}>
                {bullets.map((b, j) => (
                  <li key={j} style={vStyles.li}>{b}</li>
                ))}
              </ul>
            ) : (
              <p style={vStyles.body}>{sec.body}</p>
            )}
          </div>
        );
      })}
    </div>
  );
}

function sectionIcon(i) {
  return ["📌", "💡", "🔷", "⚡", "🎯"][i % 5];
}

const vStyles = {
  termStrip: {
    display: "flex", flexWrap: "wrap", gap: "0.4rem",
    alignItems: "center", padding: "0.6rem 0.8rem",
    background: "#f8fafc", borderRadius: "0.4rem",
    border: "1px solid #e2e8f0",
  },
  termLabel: { fontSize: "0.8rem", fontWeight: 700, color: "#475569", marginRight: "0.25rem" },
  term: {
    background: "#4f46e5", color: "#fff",
    borderRadius: 99, padding: "0.15rem 0.55rem",
    fontSize: "0.75rem", fontWeight: 600,
  },
  card: {
    borderLeft: "4px solid",
    borderRadius: "0 0.5rem 0.5rem 0",
    padding: "0.85rem 1rem",
    display: "flex", flexDirection: "column", gap: "0.4rem",
  },
  cardHead: { fontWeight: 700, fontSize: "0.9rem", margin: 0 },
  ul: { margin: 0, paddingLeft: "1.25rem", display: "flex", flexDirection: "column", gap: "0.25rem" },
  li: { fontSize: "0.875rem", color: "#374151", lineHeight: 1.6 },
  body: { fontSize: "0.875rem", color: "#374151", lineHeight: 1.7, margin: 0 },
};

// ════════════════════════════════════════════════════════════════════════════
// AUDITORY STYLE — Text-to-Speech
// ════════════════════════════════════════════════════════════════════════════
function AuditoryContent({ content, lessonTitle }) {
  const [playing, setPlaying]     = useState(false);
  const [paused, setPaused]       = useState(false);
  const [rate, setRate]           = useState(0.95);
  const [pitch, setPitch]         = useState(1);
  const [voices, setVoices]       = useState([]);
  const [voiceIdx, setVoiceIdx]   = useState(0);
  const [progress, setProgress]   = useState(0);   // 0-100
  const [supported, setSupported] = useState(true);
  const [currentWord, setCurrentWord] = useState("");
  const uttRef  = useRef(null);
  const timerRef = useRef(null);

  const words = content.split(/\s+/).length;

  useEffect(() => {
    if (!("speechSynthesis" in window)) { setSupported(false); return; }
    const load = () => {
      const v = window.speechSynthesis.getVoices().filter((v) => v.lang.startsWith("en"));
      if (v.length) setVoices(v);
    };
    load();
    window.speechSynthesis.onvoiceschanged = load;
    return () => { window.speechSynthesis.cancel(); clearInterval(timerRef.current); };
  }, []);

  const speak = useCallback(() => {
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    const utt = new SpeechSynthesisUtterance(content);
    utt.rate  = rate;
    utt.pitch = pitch;
    if (voices[voiceIdx]) utt.voice = voices[voiceIdx];

    let wordCount = 0;
    utt.onboundary = (e) => {
      if (e.name === "word") {
        wordCount++;
        const pct = Math.min(100, Math.round((wordCount / words) * 100));
        setProgress(pct);
        // highlight current word
        const spoken = content.substr(e.charIndex, e.charLength || 8);
        setCurrentWord(spoken.trim());
      }
    };
    utt.onend = () => { setPlaying(false); setPaused(false); setProgress(100); setCurrentWord(""); };
    utt.onerror = () => { setPlaying(false); setPaused(false); };

    uttRef.current = utt;
    window.speechSynthesis.speak(utt);
    setPlaying(true);
    setPaused(false);
  }, [content, rate, pitch, voices, voiceIdx, words]);

  function pause() {
    window.speechSynthesis.pause();
    setPaused(true); setPlaying(false);
  }
  function resume() {
    window.speechSynthesis.resume();
    setPaused(false); setPlaying(true);
  }
  function stop() {
    window.speechSynthesis.cancel();
    setPlaying(false); setPaused(false); setProgress(0); setCurrentWord("");
  }

  if (!supported) {
    return (
      <div>
        <StyleBanner icon="🎧" label="Auditory Mode" color="#06b6d4" bg="#ecfeff"
          desc="Text-to-speech is not supported in your browser. Try Chrome or Edge." />
        <PlainText content={content} />
      </div>
    );
  }

  const estMins = Math.ceil(words / (rate * 130));

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      <StyleBanner icon="🎧" label="Auditory Mode" color="#06b6d4" bg="#ecfeff"
        desc="Press Play to listen to the lesson. Adjust speed and voice to your preference." />

      {/* Player card */}
      <div style={aStyles.player}>
        <p style={aStyles.trackTitle}>🎙️ {lessonTitle}</p>
        <p style={aStyles.meta}>{words} words · ~{estMins} min at {rate}× speed</p>

        {/* Progress bar */}
        <div style={aStyles.barBg}>
          <div style={{ ...aStyles.barFill, width: `${progress}%` }} />
        </div>
        <p style={aStyles.wordHighlight}>{currentWord && `"${currentWord}"`}</p>

        {/* Controls */}
        <div style={aStyles.controls}>
          {!playing && !paused && (
            <button className="btn btn-primary" style={aStyles.playBtn} onClick={speak}>
              ▶ Play
            </button>
          )}
          {playing && (
            <button className="btn btn-primary" style={aStyles.playBtn} onClick={pause}>
              ⏸ Pause
            </button>
          )}
          {paused && (
            <button className="btn btn-primary" style={aStyles.playBtn} onClick={resume}>
              ▶ Resume
            </button>
          )}
          {(playing || paused) && (
            <button className="btn btn-outline" onClick={stop}>⏹ Stop</button>
          )}
        </div>

        {/* Settings */}
        <div style={aStyles.settings}>
          <label style={aStyles.setting}>
            🐢 Speed: <strong>{rate}×</strong>
            <input type="range" min="0.5" max="2" step="0.05"
              value={rate} onChange={(e) => setRate(parseFloat(e.target.value))}
              style={{ flex: 1 }} disabled={playing} />
          </label>
          <label style={aStyles.setting}>
            🎵 Pitch: <strong>{pitch}</strong>
            <input type="range" min="0.5" max="2" step="0.1"
              value={pitch} onChange={(e) => setPitch(parseFloat(e.target.value))}
              style={{ flex: 1 }} disabled={playing} />
          </label>
          {voices.length > 1 && (
            <label style={aStyles.setting}>
              🗣 Voice:
              <select value={voiceIdx}
                onChange={(e) => setVoiceIdx(Number(e.target.value))}
                style={aStyles.select} disabled={playing}>
                {voices.map((v, i) => (
                  <option key={i} value={i}>{v.name}</option>
                ))}
              </select>
            </label>
          )}
        </div>
      </div>

      {/* Show text below player for reference */}
      <details style={{ fontSize: "0.85rem" }}>
        <summary style={{ cursor: "pointer", color: "#64748b", userSelect: "none", padding: "0.25rem 0" }}>
          📄 Show transcript
        </summary>
        <PlainText content={content} />
      </details>
    </div>
  );
}

const aStyles = {
  player: {
    background: "linear-gradient(135deg,#0f172a 0%,#1e293b 100%)",
    borderRadius: "0.75rem", padding: "1.5rem",
    display: "flex", flexDirection: "column", gap: "0.75rem",
    color: "#fff",
  },
  trackTitle: { fontWeight: 700, fontSize: "1rem", margin: 0 },
  meta: { fontSize: "0.78rem", color: "#94a3b8", margin: 0 },
  barBg: { height: 6, background: "#334155", borderRadius: 99, overflow: "hidden" },
  barFill: { height: "100%", background: "linear-gradient(90deg,#4f46e5,#06b6d4)", borderRadius: 99, transition: "width 0.3s" },
  wordHighlight: { fontSize: "0.8rem", color: "#06b6d4", minHeight: "1.2em", fontStyle: "italic", margin: 0 },
  controls: { display: "flex", gap: "0.75rem", alignItems: "center" },
  playBtn: { minWidth: 100 },
  settings: { display: "flex", flexDirection: "column", gap: "0.5rem", borderTop: "1px solid #334155", paddingTop: "0.75rem" },
  setting: {
    display: "flex", alignItems: "center", gap: "0.6rem",
    fontSize: "0.8rem", color: "#cbd5e1",
  },
  select: {
    flex: 1, background: "#1e293b", color: "#fff",
    border: "1px solid #475569", borderRadius: "0.3rem", padding: "0.2rem 0.4rem",
    fontSize: "0.78rem",
  },
};

// ════════════════════════════════════════════════════════════════════════════
// READING STYLE — clean typography + summary + glossary
// ════════════════════════════════════════════════════════════════════════════
function ReadingContent({ content }) {
  const sections  = parseSections(content);
  const keyTerms  = extractKeyTerms(content);
  const wordCount = content.split(/\s+/).length;
  const readMins  = Math.ceil(wordCount / 200);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}>
      <StyleBanner icon="📖" label="Reading Mode" color="#6d28d9" bg="#ede9fe"
        desc="Optimised for focused reading with a summary and glossary." />

      {/* Reading meta */}
      <div style={rStyles.meta}>
        <span>📄 {wordCount} words</span>
        <span>⏱ ~{readMins} min read</span>
        <span>📑 {sections.length} sections</span>
      </div>

      {/* Article */}
      <article style={rStyles.article}>
        {sections.map((sec, i) => (
          <div key={i} style={{ marginBottom: "1.25rem" }}>
            {sec.heading && <h3 style={rStyles.h3}>{sec.heading}</h3>}
            {sec.body.includes("\n") ? (
              <ul style={rStyles.ul}>
                {parseBullets(sec.body).map((b, j) => (
                  <li key={j} style={rStyles.li}>{b}</li>
                ))}
              </ul>
            ) : (
              <p style={rStyles.p}>{sec.body}</p>
            )}
          </div>
        ))}
      </article>

      {/* Summary box */}
      <div style={rStyles.summaryBox}>
        <p style={rStyles.summaryTitle}>📋 Quick Summary</p>
        <ul style={rStyles.summaryList}>
          {sections.filter((s) => s.heading).slice(0, 5).map((s, i) => (
            <li key={i} style={rStyles.summaryItem}>✓ {s.heading}</li>
          ))}
          {sections.filter((s) => s.heading).length === 0 && (
            <li style={rStyles.summaryItem}>✓ {sections[0]?.body?.slice(0, 80)}…</li>
          )}
        </ul>
      </div>

      {/* Glossary */}
      {keyTerms.length > 0 && (
        <div style={rStyles.glossary}>
          <p style={rStyles.glossaryTitle}>📚 Key Terms in this Lesson</p>
          <div style={rStyles.termGrid}>
            {keyTerms.map((t) => (
              <span key={t} style={rStyles.termChip}>{t}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

const rStyles = {
  meta: {
    display: "flex", gap: "1.25rem", fontSize: "0.8rem",
    color: "#64748b", padding: "0.5rem 0",
    borderBottom: "1px solid #e2e8f0",
  },
  article: { fontFamily: "Georgia, 'Times New Roman', serif" },
  h3: { fontSize: "1rem", fontWeight: 700, color: "#1e293b", marginBottom: "0.4rem" },
  p: { fontSize: "0.95rem", color: "#334155", lineHeight: 1.9, margin: 0 },
  ul: { paddingLeft: "1.5rem", margin: 0, display: "flex", flexDirection: "column", gap: "0.3rem" },
  li: { fontSize: "0.9rem", color: "#334155", lineHeight: 1.7 },
  summaryBox: {
    background: "#fefce8", border: "1px solid #fde68a",
    borderRadius: "0.5rem", padding: "1rem",
  },
  summaryTitle: { fontWeight: 700, fontSize: "0.875rem", color: "#92400e", marginBottom: "0.5rem" },
  summaryList: { margin: 0, paddingLeft: "1rem", display: "flex", flexDirection: "column", gap: "0.25rem" },
  summaryItem: { fontSize: "0.85rem", color: "#78350f" },
  glossary: {
    background: "#f8fafc", border: "1px solid #e2e8f0",
    borderRadius: "0.5rem", padding: "1rem",
  },
  glossaryTitle: { fontWeight: 700, fontSize: "0.875rem", color: "#1e293b", marginBottom: "0.6rem" },
  termGrid: { display: "flex", flexWrap: "wrap", gap: "0.4rem" },
  termChip: {
    background: "#e0e7ff", color: "#3730a3",
    borderRadius: 99, padding: "0.2rem 0.65rem",
    fontSize: "0.78rem", fontWeight: 600,
  },
};

// ════════════════════════════════════════════════════════════════════════════
// KINESTHETIC STYLE — interactive fill-in-the-blank exercises
// ════════════════════════════════════════════════════════════════════════════
function KinestheticContent({ content }) {
  const exercises = buildExercises(content);
  const [answers, setAnswers]     = useState({});
  const [checked, setChecked]     = useState({});
  const [showText, setShowText]   = useState(false);
  const [allDone, setAllDone]     = useState(false);

  function handleInput(i, val) {
    setAnswers((a) => ({ ...a, [i]: val }));
    setChecked((c) => ({ ...c, [i]: undefined })); // reset check when typing
  }

  function checkAnswer(i) {
    const correct = answers[i]?.trim().toLowerCase() === exercises[i].answer.toLowerCase();
    setChecked((c) => ({ ...c, [i]: correct }));
    // check if all done
    const newChecked = { ...checked, [i]: correct };
    if (exercises.every((_, j) => newChecked[j] !== undefined)) setAllDone(true);
  }

  function reset() {
    setAnswers({}); setChecked({}); setAllDone(false);
  }

  const score = Object.values(checked).filter(Boolean).length;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      <StyleBanner icon="🖐️" label="Kinesthetic Mode" color="#16a34a" bg="#dcfce7"
        desc="Learn by doing — fill in the blanks to test your understanding as you read." />

      {exercises.length > 0 ? (
        <>
          <p style={{ fontSize: "0.85rem", color: "#64748b" }}>
            Complete the {exercises.length} exercises below. Type your answer and click Check.
          </p>

          {exercises.map((ex, i) => {
            const result = checked[i];
            return (
              <div key={i} style={{
                ...kStyles.card,
                borderColor: result === true ? "#22c55e" : result === false ? "#ef4444" : "#e2e8f0",
                background: result === true ? "#f0fdf4" : result === false ? "#fef2f2" : "#fff",
              }}>
                <p style={kStyles.num}>Exercise {i + 1}</p>
                <p style={kStyles.sentence}>
                  {ex.sentence.replace("________",
                    result === true
                      ? `✅ ${ex.answer}`
                      : result === false
                        ? `❌ ${answers[i] || "________"}`
                        : "________"
                  )}
                </p>

                {result === undefined && (
                  <div style={kStyles.inputRow}>
                    <input
                      type="text"
                      placeholder="Your answer…"
                      value={answers[i] || ""}
                      onChange={(e) => handleInput(i, e.target.value)}
                      onKeyDown={(e) => e.key === "Enter" && checkAnswer(i)}
                      style={kStyles.input}
                      autoComplete="off"
                    />
                    <button className="btn btn-primary" onClick={() => checkAnswer(i)}
                      disabled={!answers[i]?.trim()} style={{ fontSize: "0.85rem" }}>
                      Check
                    </button>
                  </div>
                )}

                {result === false && (
                  <div style={kStyles.hint}>
                    💡 Hint: the answer starts with "<strong>{ex.answer[0]}</strong>"
                    <button className="btn btn-secondary" style={{ fontSize: "0.75rem", marginLeft: 8 }}
                      onClick={() => setChecked((c) => ({ ...c, [i]: undefined }))}>
                      Try again
                    </button>
                  </div>
                )}

                {result === true && (
                  <p style={{ fontSize: "0.8rem", color: "#15803d", margin: 0 }}>🎉 Correct!</p>
                )}
              </div>
            );
          })}

          {allDone && (
            <div style={kStyles.scoreCard}>
              <p style={kStyles.scoreTitle}>
                {score === exercises.length ? "🏆 Perfect score!" : score >= exercises.length / 2 ? "👍 Good effort!" : "📖 Keep practising!"}
              </p>
              <p style={kStyles.scoreNum}>{score} / {exercises.length} correct</p>
              <button className="btn btn-outline" onClick={reset} style={{ fontSize: "0.85rem" }}>
                🔄 Try Again
              </button>
            </div>
          )}
        </>
      ) : (
        <p style={{ color: "#64748b", fontSize: "0.875rem" }}>
          No exercises could be generated for this lesson. Read the content below.
        </p>
      )}

      {/* Full text always available */}
      <details open={exercises.length === 0}>
        <summary style={{ cursor: "pointer", color: "#64748b", fontSize: "0.85rem", userSelect: "none", padding: "0.25rem 0" }}>
          📄 {showText ? "Hide" : "Show"} full lesson text
        </summary>
        <PlainText content={content} />
      </details>
    </div>
  );
}

const kStyles = {
  card: {
    border: "2px solid", borderRadius: "0.5rem",
    padding: "1rem", display: "flex", flexDirection: "column", gap: "0.5rem",
    transition: "border-color 0.2s, background 0.2s",
  },
  num: { fontSize: "0.72rem", fontWeight: 700, color: "#64748b", textTransform: "uppercase", margin: 0 },
  sentence: { fontSize: "0.95rem", color: "#1e293b", lineHeight: 1.7, margin: 0 },
  inputRow: { display: "flex", gap: "0.5rem", alignItems: "center" },
  input: {
    flex: 1, padding: "0.5rem 0.75rem",
    border: "1.5px solid #e2e8f0", borderRadius: "0.4rem",
    fontSize: "0.9rem", outline: "none",
  },
  hint: { fontSize: "0.82rem", color: "#b45309", display: "flex", alignItems: "center" },
  scoreCard: {
    textAlign: "center", background: "#f8fafc",
    borderRadius: "0.5rem", padding: "1.25rem",
    border: "1px solid #e2e8f0",
    display: "flex", flexDirection: "column", alignItems: "center", gap: "0.5rem",
  },
  scoreTitle: { fontWeight: 700, fontSize: "1.1rem", margin: 0 },
  scoreNum: { fontSize: "1.5rem", fontWeight: 800, color: "#4f46e5", margin: 0 },
};

// ════════════════════════════════════════════════════════════════════════════
// SHARED helpers
// ════════════════════════════════════════════════════════════════════════════
function StyleBanner({ icon, label, color, bg, desc }) {
  return (
    <div style={{ background: bg, border: `1px solid ${color}33`, borderRadius: "0.4rem", padding: "0.6rem 0.9rem", display: "flex", gap: "0.6rem", alignItems: "flex-start" }}>
      <span style={{ fontSize: "1.2rem" }}>{icon}</span>
      <div>
        <p style={{ fontSize: "0.78rem", fontWeight: 700, color, margin: 0 }}>{label}</p>
        <p style={{ fontSize: "0.75rem", color: "#64748b", margin: 0 }}>{desc}</p>
      </div>
    </div>
  );
}

function PlainText({ content }) {
  return (
    <p style={{ fontSize: "0.875rem", color: "#475569", lineHeight: 1.9, whiteSpace: "pre-line", marginTop: "0.5rem" }}>
      {content}
    </p>
  );
}

// ════════════════════════════════════════════════════════════════════════════
// MAIN EXPORT — picks the right renderer based on learning style
// ════════════════════════════════════════════════════════════════════════════
export default function LessonContent({ content, lessonTitle }) {
  const { user } = useAuth();
  const style = user?.learning_style || "visual";

  if (!content) {
    return <p style={{ color: "#94a3b8", fontStyle: "italic" }}>No content available for this lesson.</p>;
  }

  switch (style) {
    case "auditory":    return <AuditoryContent    content={content} lessonTitle={lessonTitle} />;
    case "reading":     return <ReadingContent     content={content} />;
    case "kinesthetic": return <KinestheticContent content={content} />;
    default:            return <VisualContent      content={content} />;
  }
}
