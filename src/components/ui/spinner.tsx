// src/components/ui/spinner.tsx
import { Loader2 } from "lucide-react"
import { cn } from "@/lib/utils"

export interface SpinnerProps extends React.HTMLAttributes<HTMLDivElement> {}

export function Spinner({ className, ...props }: SpinnerProps) {
  return (
    <div className={cn("flex items-center justify-center", className)} {...props}>
      <Loader2 className="h-full w-full animate-spin text-primary" />
    </div>
  )
}
