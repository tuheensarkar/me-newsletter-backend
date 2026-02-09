// src/app/layout.js
export const metadata = {
  title: 'ME Newsletter',
  description: 'Stay updated with the latest news and insights',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}