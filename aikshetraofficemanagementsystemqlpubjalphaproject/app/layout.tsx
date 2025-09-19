import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "../src/index.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Aikshetra Office Management System",
  description: "Comprehensive office management system for employee tracking, attendance, tasks, and more",
    generator: 'v0.app'
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
