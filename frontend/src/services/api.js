import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL || "/api";

const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// Attach JWT on every request if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// On 401, clear session and redirect to login
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

// ── Auth ──────────────────────────────────────────────────────────────────────
export const authApi = {
  register: (data) => api.post("/auth/register", data),
  login: (data) => api.post("/auth/login", data),
};

// ── Users ─────────────────────────────────────────────────────────────────────
export const usersApi = {
  me: () => api.get("/users/me"),
  list: () => api.get("/users/"),
  updateProfile: (data) => api.patch("/users/me", data),
};

// ── Courses ───────────────────────────────────────────────────────────────────
export const coursesApi = {
  list: () => api.get("/courses/"),
  get: (id) => api.get(`/courses/${id}`),
  create: (data) => api.post("/courses/", null, { params: data }),
};

// ── Lessons ───────────────────────────────────────────────────────────────────
export const lessonsApi = {
  list: (courseId) =>
    api.get("/lessons/", courseId ? { params: { course_id: courseId } } : {}),
  get: (id) => api.get(`/lessons/${id}`),
  create: (data) => api.post("/lessons/", null, { params: data }),
};

// ── Quizzes ───────────────────────────────────────────────────────────────────
export const quizzesApi = {
  get: (id) => api.get(`/quizzes/${id}`),
  byLesson: (lessonId) => api.get(`/quizzes/by-lesson/${lessonId}`),
  create: (data) => api.post("/quizzes/", null, { params: data }),
  submit: (id, answers) => api.post(`/quizzes/${id}/submit`, answers),
};

// ── Attempts ──────────────────────────────────────────────────────────────────
export const attemptsApi = {
  start: (userId, quizId) =>
    api.post("/attempts/start", null, { params: { user_id: userId, quiz_id: quizId } }),
  answer: (attemptId, questionId, selectedAnswer) =>
    api.post(`/attempts/${attemptId}/answer`, null, {
      params: { question_id: questionId, selected_answer: selectedAnswer },
    }),
  get: (id) => api.get(`/attempts/${id}`),
};

// ── Recommendations ───────────────────────────────────────────────────────────
export const recommendationsApi = {
  get: (userId, quizId) =>
    api.get("/recommendations/", { params: { user_id: userId, quiz_id: quizId } }),
  difficulty: (score) =>
    api.get("/recommendations/difficulty", { params: { score } }),
  questions: (quizId, difficulty) =>
    api.get("/recommendations/questions", { params: { quiz_id: quizId, difficulty } }),
};

// ── Feedback ──────────────────────────────────────────────────────────────────
export const feedbackApi = {
  get: (userId, quizId) =>
    api.get("/feedback/", { params: { user_id: userId, quiz_id: quizId } }),
};

export default api;
