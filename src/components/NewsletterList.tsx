// src/components/NewsletterList.tsx
import { useState } from 'react'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './ui/card'
import { Button } from './ui/button'

interface Newsletter {
  id: number | string
  title: string
  description: string
  content?: string
  publish: string
  time_to_read?: number
}

interface NewsletterListProps {
  newsletters: Newsletter[]
}

export default function NewsletterList({ newsletters }: NewsletterListProps) {
  const [expandedId, setExpandedId] = useState<number | string | null>(null)

  if (!newsletters || newsletters.length === 0) {
    return (
      <Card className="p-8 text-center animate-fade-in">
        <p className="text-muted-foreground">No newsletters available yet.</p>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      {newsletters.map((newsletter) => (
        <Card key={newsletter.id} className="overflow-hidden hover:shadow-md transition-shadow animate-fade-in">
          <CardContent className="p-6">
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <CardTitle className="text-xl font-bold mb-2">
                  {newsletter.title}
                </CardTitle>
                <CardDescription className="text-base mb-4">
                  {newsletter.description}
                </CardDescription>
                
                {expandedId === newsletter.id && (
                  <div className="prose prose-teal max-w-none mb-4 animate-fade-in">
                    <div 
                      dangerouslySetInnerHTML={{ 
                        __html: newsletter.content || '<p>No content available</p>' 
                      }} 
                    />
                  </div>
                )}
                
                <div className="flex justify-between items-center text-sm text-muted-foreground">
                  <span>
                    {new Date(newsletter.publish).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}
                  </span>
                  {newsletter.time_to_read && (
                    <span className="bg-secondary text-secondary-foreground px-2 py-0.5 rounded-full text-xs">
                      {newsletter.time_to_read} min read
                    </span>
                  )}
                </div>
              </div>
              
              <Button
                variant="ghost"
                onClick={() => setExpandedId(expandedId === newsletter.id ? null : newsletter.id)}
                className="ml-4 text-primary hover:text-primary/80"
              >
                {expandedId === newsletter.id ? 'Show Less' : 'Read More'}
              </Button>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
