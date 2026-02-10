// src/lib/api.ts
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Mock data as fallback
const MOCK_NEWSLETTERS = [
  {
    id: 1,
    title: "The Future of AI in Newsletters",
    description: "Exploring how LLMs are changing the way we consume content.",
    content: "<p>Artificial intelligence is revolutionizing the newsletter industry. From automated summarization to hyper-personalized content, the possibilities are endless...</p>",
    publish: new Date().toISOString(),
    time_to_read: 5
  },
  {
    id: 2,
    title: "Sustainable Tech Trends 2026",
    description: "Why green computing is no longer optional for major tech firms.",
    content: "<p>As energy costs rise and climate impact becomes a primary concern for investors, tech companies are pivoting towards sustainable hardware and efficient algorithms...</p>",
    publish: new Date(Date.now() - 86400000).toISOString(),
    time_to_read: 8
  },
  {
    id: 3,
    title: "Remote Work: 5 Years Later",
    description: "A deep dive into how distributed teams have evolved since the global shift.",
    content: "<p>Five years ago, the world embarked on a massive experiment in remote work. Today, we examine the lasting impacts on culture, productivity, and urban development...</p>",
    publish: new Date(Date.now() - 172800000).toISOString(),
    time_to_read: 6
  }
]

// Newsletter API endpoints
export const newsletterService = {
  getAll: async () => {
    try {
      const res = await api.get('/newsletters/')
      return res.data.result || MOCK_NEWSLETTERS
    } catch (err) {
      console.warn('Backend not reachable, using mock data')
      return MOCK_NEWSLETTERS
    }
  },
  getRecent: async () => {
    try {
      const res = await api.get('/newsletters/recent/')
      return res.data.result || MOCK_NEWSLETTERS.slice(0, 2)
    } catch (err) {
      return MOCK_NEWSLETTERS.slice(0, 2)
    }
  },
  getBySlug: (slug: string) => api.get(`/newsletters/${slug}/`).then(res => res.data.result),
}

// Subscription API endpoints
export const subscriptionService = {
  subscribe: async (email: string) => {
    try {
      const res = await api.post('/subscribe/', { email })
      return res.data
    } catch (err) {
      console.warn('Backend not reachable, mocking success')
      return { status: 'success', message: 'Subscribed successfully!' }
    }
  },
}

export default api
