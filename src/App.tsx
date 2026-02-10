// src/App.tsx
import { useState, useEffect } from 'react'
import NewsletterList from './components/NewsletterList'
import SubscribeForm from './components/SubscribeForm'
import { newsletterService } from './lib/api'
import { Card, CardContent } from './components/ui/card'
import { Spinner } from './components/ui/spinner'

function App() {
  const [newsletters, setNewsletters] = useState([])
  const [recentNewsletters, setRecentNewsletters] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
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
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <Spinner className="h-12 w-12 text-primary mx-auto" />
          <p className="mt-4 text-muted-foreground animate-pulse">Loading newsletters...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background text-foreground font-sans">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <div className="text-center sm:text-left">
              <h1 className="text-3xl font-bold font-serif text-primary tracking-tight">ME Newsletter</h1>
              <p className="text-muted-foreground mt-1">Stay updated with the latest news and insights</p>
            </div>
            <div className="flex gap-4">
              <button className="text-sm font-medium hover:text-primary transition-colors">Archive</button>
              <button className="text-sm font-medium hover:text-primary transition-colors">About</button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        {/* Error Message */}
        {error && (
          <Card className="bg-destructive/5 border-destructive/20 mb-8 animate-fade-in">
            <CardContent className="p-4 flex items-center gap-3 text-destructive">
              <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <p className="font-medium text-sm">{error}</p>
            </CardContent>
          </Card>
        )}

        {/* Subscribe Section */}
        <section className="bg-secondary rounded-2xl p-8 sm:p-12 mb-16 text-center border shadow-sm relative overflow-hidden">
          <div className="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 bg-primary/10 rounded-full blur-2xl" />
          <div className="absolute bottom-0 left-0 -mb-4 -ml-4 h-24 w-24 bg-accent/20 rounded-full blur-2xl" />
          
          <div className="relative z-0">
            <h2 className="text-2xl sm:text-3xl font-bold text-secondary-foreground mb-3 font-serif">Never Miss an Update</h2>
            <p className="text-muted-foreground mb-8 max-w-md mx-auto">Join 10,000+ readers and get the best content delivered to your inbox every week.</p>
            <SubscribeForm />
          </div>
        </section>

        {/* Recent Newsletters */}
        {recentNewsletters.length > 0 && (
          <section className="mb-16">
            <div className="flex items-center gap-4 mb-8">
              <h2 className="text-2xl font-bold font-serif">Recent Highlights</h2>
              <div className="h-px bg-border flex-1" />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {recentNewsletters.map((newsletter: any) => (
                <Card key={newsletter.id} className="group hover:scale-[1.02] transition-transform cursor-pointer border-none shadow-md bg-white">
                  <CardContent className="p-0">
                    <div className="h-48 bg-secondary flex items-center justify-center group-hover:bg-secondary/80 transition-colors">
                      <span className="text-4xl">📰</span>
                    </div>
                    <div className="p-6">
                      <h3 className="text-xl font-bold mb-2 group-hover:text-primary transition-colors">
                        {newsletter.title}
                      </h3>
                      <p className="text-muted-foreground text-sm line-clamp-2 mb-4">
                        {newsletter.description}
                      </p>
                      <div className="flex items-center text-xs text-muted-foreground">
                        <span>{new Date(newsletter.publish).toLocaleDateString()}</span>
                        <span className="mx-2">•</span>
                        <span>{newsletter.time_to_read} min read</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>
        )}

        {/* All Newsletters */}
        <section>
          <div className="flex items-center gap-4 mb-8">
            <h2 className="text-2xl font-bold font-serif">Past Issues</h2>
            <div className="h-px bg-border flex-1" />
          </div>
          <NewsletterList newsletters={newsletters} />
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-secondary/50 border-t py-12 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 text-center md:text-left">
            <div className="col-span-1">
              <h3 className="text-xl font-bold font-serif text-primary mb-4">ME Newsletter</h3>
              <p className="text-muted-foreground text-sm">Providing quality insights and news since 2023. Our mission is to keep you informed and inspired.</p>
            </div>
            <div className="col-span-1">
              <h4 className="font-bold mb-4 text-sm uppercase tracking-wider">Quick Links</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-primary">Home</a></li>
                <li><a href="#" className="hover:text-primary">Archive</a></li>
                <li><a href="#" className="hover:text-primary">About Us</a></li>
                <li><a href="#" className="hover:text-primary">Contact</a></li>
              </ul>
            </div>
            <div className="col-span-1">
              <h4 className="font-bold mb-4 text-sm uppercase tracking-wider">Follow Us</h4>
              <div className="flex justify-center md:justify-start gap-4">
                <a href="#" className="h-8 w-8 bg-white rounded-full flex items-center justify-center border hover:border-primary hover:text-primary transition-all">𝕏</a>
                <a href="#" className="h-8 w-8 bg-white rounded-full flex items-center justify-center border hover:border-primary hover:text-primary transition-all">in</a>
                <a href="#" className="h-8 w-8 bg-white rounded-full flex items-center justify-center border hover:border-primary hover:text-primary transition-all">fb</a>
              </div>
            </div>
          </div>
          <div className="border-t mt-12 pt-8 text-center text-xs text-muted-foreground">
            <p>&copy; 2026 ME Newsletter. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
