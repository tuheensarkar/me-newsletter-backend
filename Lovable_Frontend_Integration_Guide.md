# Lovable Frontend Integration Guide

## Quick Start for Lovable Development

### 1. Create New Lovable Project

1. Go to [Lovable.dev](https://lovable.dev)
2. Click "New Project"
3. Choose "Next.js App" template
4. Name your project (e.g., "me-newsletter-frontend")

### 2. Project Structure Setup

```
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── api/
├── components/
│   ├── layout/
│   │   ├── Header.tsx
│   │   └── Footer.tsx
│   ├── newsletter/
│   │   ├── NewsletterList.tsx
│   │   ├── NewsletterCard.tsx
│   │   └── NewsletterDetail.tsx
│   └── ui/
│       ├── Button.tsx
│       └── Input.tsx
├── lib/
│   ├── api.ts
│   └── types.ts
└── hooks/
    └── useNewsletters.ts
```

### 3. Essential Dependencies

```bash
npm install @tanstack/react-query axios date-fns
npm install -D @types/node @types/react
```

### 4. API Client Setup

**File: `src/lib/api.ts`**
```typescript
import axios from 'axios'

// Configure axios instance
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for authentication
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API endpoints
export const newsletterApi = {
  getAll: () => api.get('/newsletters/'),
  getRecent: () => api.get('/newsletters/recent/'),
  getBySlug: (slug: string) => api.get(`/newsletters/${slug}/`),
  getPrevious: () => api.get('/newsletters/previous/'),
}

export const subscribeApi = {
  subscribe: (email: string) => 
    api.post('/subscribe/', { email }),
}

export const healthApi = {
  getStatus: () => api.get('/status/'),
  getHealth: () => api.get('/health/'),
}

export default api
```

### 5. TypeScript Types

**File: `src/lib/types.ts`**
```typescript
export interface Newsletter {
  id: number
  title: string
  slug: string
  description: string
  content: string
  publish: string
  created: string
  modified: string
  image?: string
  image_alt?: string
  region?: string
  country?: string
  time_to_read: number
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface ApiResponse<T> {
  result: T
}

export interface SubscribeFormData {
  email: string
}
```

### 6. React Query Hooks

**File: `src/hooks/useNewsletters.ts`**
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { newsletterApi, subscribeApi } from '@/lib/api'
import { Newsletter, SubscribeFormData } from '@/lib/types'

// Fetch all newsletters
export const useNewsletters = () => {
  return useQuery<Newsletter[]>({
    queryKey: ['newsletters'],
    queryFn: async () => {
      const response = await newsletterApi.getAll()
      return response.data.result
    },
    staleTime: 1000 * 60 * 5, // 5 minutes
  })
}

// Fetch recent newsletters
export const useRecentNewsletters = () => {
  return useQuery<Newsletter[]>({
    queryKey: ['recent-newsletters'],
    queryFn: async () => {
      const response = await newsletterApi.getRecent()
      return response.data.result
    },
    staleTime: 1000 * 60 * 10, // 10 minutes
  })
}

// Fetch newsletter by slug
export const useNewsletterBySlug = (slug: string) => {
  return useQuery<Newsletter[]>({
    queryKey: ['newsletter', slug],
    queryFn: async () => {
      const response = await newsletterApi.getBySlug(slug)
      return response.data.result
    },
    enabled: !!slug,
  })
}

// Subscribe to newsletter
export const useSubscribe = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (data: SubscribeFormData) => {
      const response = await subscribeApi.subscribe(data.email)
      return response.data
    },
    onSuccess: () => {
      // Invalidate and refetch subscriptions if needed
      queryClient.invalidateQueries({ queryKey: ['subscriptions'] })
    },
  })
}
```

### 7. Core Components

**File: `src/components/newsletter/NewsletterCard.tsx`**
```tsx
import Link from 'next/link'
import { Newsletter } from '@/lib/types'
import { format } from 'date-fns'

interface NewsletterCardProps {
  newsletter: Newsletter
}

export default function NewsletterCard({ newsletter }: NewsletterCardProps) {
  return (
    <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
      {newsletter.image && (
        <img 
          src={newsletter.image} 
          alt={newsletter.image_alt || newsletter.title}
          className="w-full h-48 object-cover rounded-md mb-4"
        />
      )}
      <h3 className="text-xl font-bold mb-2">
        <Link href={`/newsletter/${newsletter.slug}`} className="hover:text-blue-600">
          {newsletter.title}
        </Link>
      </h3>
      <p className="text-gray-600 mb-3">{newsletter.description}</p>
      <div className="flex justify-between items-center text-sm text-gray-500">
        <span>{format(new Date(newsletter.publish), 'MMMM d, yyyy')}</span>
        <span>{newsletter.time_to_read} min read</span>
      </div>
    </div>
  )
}
```

**File: `src/components/newsletter/NewsletterList.tsx`**
```tsx
import { useNewsletters } from '@/hooks/useNewsletters'
import NewsletterCard from './NewsletterCard'
import { Alert, AlertDescription } from '@/components/ui/Alert'

export default function NewsletterList() {
  const { data: newsletters, isLoading, error } = useNewsletters()

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="border rounded-lg p-6 animate-pulse">
            <div className="h-48 bg-gray-200 rounded-md mb-4"></div>
            <div className="h-6 bg-gray-200 rounded mb-2"></div>
            <div className="h-4 bg-gray-200 rounded mb-3"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertDescription>
          Failed to load newsletters. Please try again later.
        </AlertDescription>
      </Alert>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {newsletters?.map((newsletter) => (
        <NewsletterCard key={newsletter.id} newsletter={newsletter} />
      ))}
    </div>
  )
}
```

### 8. Main Page Implementation

**File: `src/app/page.tsx`**
```tsx
'use client'

import NewsletterList from '@/components/newsletter/NewsletterList'
import { useRecentNewsletters } from '@/hooks/useNewsletters'
import SubscribeForm from '@/components/SubscribeForm'

export default function HomePage() {
  const { data: recentNewsletters } = useRecentNewsletters()

  return (
    <main className="container mx-auto px-4 py-8">
      {/* Hero Section */}
      <section className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">ME Newsletter</h1>
        <p className="text-xl text-gray-600 mb-8">
          Stay updated with the latest news and insights
        </p>
        <SubscribeForm />
      </section>

      {/* Recent Newsletters */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Recent Issues</h2>
        {recentNewsletters && recentNewsletters.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {recentNewsletters.map((newsletter) => (
              <div key={newsletter.id} className="border rounded-lg p-6">
                <h3 className="text-xl font-semibold mb-2">{newsletter.title}</h3>
                <p className="text-gray-600 mb-4">{newsletter.description}</p>
                <a 
                  href={`/newsletter/${newsletter.slug}`}
                  className="text-blue-600 hover:underline"
                >
                  Read more →
                </a>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No recent newsletters available.</p>
        )}
      </section>

      {/* All Newsletters */}
      <section>
        <h2 className="text-2xl font-bold mb-6">All Issues</h2>
        <NewsletterList />
      </section>
    </main>
  )
}
```

### 9. Environment Variables

**File: `.env.local`**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1/
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

**File: `.env.production`**
```env
NEXT_PUBLIC_API_URL=https://your-django-backend-domain.com/api/v1/
NEXT_PUBLIC_SITE_URL=https://your-lovable-app.lovable.dev
```

### 10. Deployment Configuration

**File: `next.config.js`**
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['your-image-domain.com'], // Add your media domain
  },
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Credentials', value: 'true' },
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,POST,PUT,PATCH,DELETE,OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version' },
        ]
      }
    ]
  }
}

module.exports = nextConfig
```

### 11. Testing the Integration

1. Start your Django backend:
```bash
python manage.py runserver
```

2. Start your Lovable frontend:
```bash
npm run dev
```

3. Test API endpoints:
- Visit `http://localhost:3000/api/status` to verify API connectivity
- Check `http://localhost:3000/api/health` for health status

### 12. Deployment Steps

1. **Build the frontend:**
```bash
npm run build
```

2. **Deploy to Lovable:**
- Push code to connected GitHub repository
- Lovable will automatically build and deploy

3. **Configure environment variables in Lovable dashboard:**
- `NEXT_PUBLIC_API_URL` - Your Django backend URL
- `NEXT_PUBLIC_SITE_URL` - Your Lovable app URL

4. **Set up domain and SSL:**
- Configure custom domain in Lovable dashboard
- SSL certificate is automatically provisioned

### 13. Monitoring and Maintenance

- Monitor API response times
- Set up error tracking with Sentry
- Configure uptime monitoring
- Regular security updates
- Performance optimization

This setup provides a solid foundation for migrating your Django newsletter application's frontend to Lovable while maintaining API connectivity with your existing backend.