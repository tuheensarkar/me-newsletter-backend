// src/components/NewsletterList.js
'use client'

import { useState } from 'react'

export default function NewsletterList({ newsletters }) {
  const [expandedId, setExpandedId] = useState(null)

  if (!newsletters || newsletters.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8 text-center">
        <p className="text-gray-500">No newsletters available yet.</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {newsletters.map((newsletter) => (
        <div key={newsletter.id} className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="p-6">
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {newsletter.title}
                </h3>
                <p className="text-gray-600 mb-4">
                  {newsletter.description}
                </p>
                
                {/* Expandable content */}
                {expandedId === newsletter.id && (
                  <div className="prose max-w-none mb-4">
                    <div 
                      dangerouslySetInnerHTML={{ 
                        __html: newsletter.content || '<p>No content available</p>' 
                      }} 
                    />
                  </div>
                )}
                
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
              
              <button
                onClick={() => setExpandedId(expandedId === newsletter.id ? null : newsletter.id)}
                className="ml-4 text-blue-600 hover:text-blue-800 font-medium"
              >
                {expandedId === newsletter.id ? 'Show Less' : 'Read More'}
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}