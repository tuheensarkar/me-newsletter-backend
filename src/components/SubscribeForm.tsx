// src/components/SubscribeForm.tsx
import { useState } from 'react'
import { Input } from './ui/input'
import { Button } from './ui/button'
import { subscriptionService } from '../lib/api'
import { toast } from 'react-hot-toast'
import { Loader2, Mail } from 'lucide-react'

export default function SubscribeForm() {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!email) return

    setLoading(true)
    try {
      await subscriptionService.subscribe(email)
      toast.success('Thanks for subscribing!')
      setEmail('')
    } catch (err) {
      toast.error('Failed to subscribe. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3 max-w-lg mx-auto">
      <div className="relative flex-1">
        <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="pl-10"
          disabled={loading}
        />
      </div>
      <Button type="submit" disabled={loading} className="min-w-[120px]">
        {loading ? (
          <Loader2 className="h-4 w-4 animate-spin mr-2" />
        ) : null}
        Subscribe
      </Button>
    </form>
  )
}
