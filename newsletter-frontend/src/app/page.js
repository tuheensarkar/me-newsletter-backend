// src/app/page.js
'use client'

import { useState, useEffect } from 'react'
import NewsletterList from '../components/NewsletterList'
import SubscribeForm from '../components/SubscribeForm'
import { newsletterService, healthService } from '../lib/api'

export default function Home() {
  const [newsletters, setNewsletters] = useState([])
  const [recentNewsletters, setRecentNewsletters] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        // Test API connectivity
        await healthService.getStatus()
        
        // Fetch newsletters
        const [allNewsletters, recentNews] = await Promise.all([
          newsletterService.getAll(),
          newsletterService.getRecent()
        ])
        
        setNewsletters(allNewsletters || [])
        setRecentNewsletters(recentNews || [])
        setError(null)
      } catch (err) {
        console.error('Failed to fetch data:', err)
        setError('Failed to load newsletters. Please try again later.')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading newsletters...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900">ME Newsletter</h1>
            <p className="mt-2 text-xl text-gray-600">
              Stay updated with the latest news and insights
            </p>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Connection Error</h3>
                <div className="mt-2 text-sm text-red-700">
                  <p>{error}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Subscribe Section */}
        <section className="bg-white rounded-lg shadow-md p-6 mb-12">
          <div className="text-center">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Never Miss an Update</h2>
            <SubscribeForm />
          </div>
        </section>

        {/* Recent Newsletters */}
        {recentNewsletters.length > 0 && (
          <section className="mb-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Recent Issues</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {recentNewsletters.map((newsletter) => (
                <div key={newsletter.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                  <div className="p-6">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      {newsletter.title}
                    </h3>
                    <p className="text-gray-600 mb-4">
                      {newsletter.description}
                    </p>
                    <div className="flex justify-between items-center text-sm text-gray-500">
                      <span>
                        {new Date(newsletter.publish).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric'
                        })}
                      </span>
                      {newsletter.time_to_read && (
                        <span>{newsletter.time_to_read} min read</span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* All Newsletters */}
        <section>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">All Issues</h2>
          <NewsletterList newsletters={newsletters} />
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p>&copy; 2026 ME Newsletter. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}