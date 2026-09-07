import React from "react";

const OPTION_LABELS = ["A", "B", "C", "D"];

export default function QuizQuestion({
  question,
  questionNumber,
  totalQuestions,
  selectedAnswer,
  onSelect,
  disabled = false,
}) {
  const options = [
    question.option_a,
    question.option_b,
    question.option_c,
    question.option_d,
  ];

  return (
    <div style={styles.wrapper}>
      <p style={styles.counter}>
        Question {questionNumber} of {totalQuestions}
      </p>
      <h3 style={styles.text}>{question.question_text || question.question}</h3>

      <div style={styles.options}>
        {options.map((opt, i) => {
          const label = OPTION_LABELS[i];
          const selected = selectedAnswer === label;
          return (
            <button
              key={label}
              onClick={() => !disabled && onSelect(label)}
              disabled={disabled}
              aria-pressed={selected}
              style={{
                ...styles.option,
                ...(selected ? styles.optionSelected : {}),
                ...(disabled ? styles.optionDisabled : {}),
              }}
            >
              <span style={{ ...styles.bubble, ...(selected ? styles.bubbleSelected : {}) }}>
                {label}
              </span>
              <span>{opt}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}

const styles = {
  wrapper: { display: "flex", flexDirection: "column", gap: "1rem" },
  counter: { fontSize: "0.8rem", color: "#64748b", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.05em" },
  text: { fontSize: "1.1rem", fontWeight: 600, color: "#1e293b", lineHeight: 1.5 },
  options: { display: "flex", flexDirection: "column", gap: "0.6rem" },
  option: {
    display: "flex",
    alignItems: "center",
    gap: "0.75rem",
    padding: "0.75rem 1rem",
    border: "1.5px solid #e2e8f0",
    borderRadius: "0.5rem",
    background: "#fff",
    textAlign: "left",
    fontSize: "0.9rem",
    color: "#1e293b",
    cursor: "pointer",
    transition: "border-color 0.15s, background 0.15s",
  },
  optionSelected: {
    borderColor: "#4f46e5",
    background: "#eef2ff",
  },
  optionDisabled: { cursor: "default", opacity: 0.7 },
  bubble: {
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    width: 28,
    height: 28,
    borderRadius: "50%",
    background: "#f1f5f9",
    color: "#475569",
    fontWeight: 700,
    fontSize: "0.8rem",
    flexShrink: 0,
  },
  bubbleSelected: { background: "#4f46e5", color: "#fff" },
};
