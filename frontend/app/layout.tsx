import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Note Taker AI | Transcribe & Summarize",
  description: "Record, transcribe, and summarize your audio notes with AI-powered technology",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <div className="min-h-screen bg-background">
          <header className="border-b">
            <div className="container mx-auto px-4 py-4">
              <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold">
                  Note Taker <span className="text-primary">AI</span>
                </h1>
                <p className="text-sm text-muted-foreground hidden sm:block">
                  built with AssemblyAI & OpenAI | powered by Render.com
                </p>
              </div>
            </div>
          </header>
          <main className="container mx-auto px-4 py-8">
            {children}
          </main>
          <footer className="border-t mt-16">
            <div className="container mx-auto px-4 py-6 text-center text-sm text-muted-foreground">
              <p>built with AssemblyAI & OpenAI | powered by <a href="https://render.com" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline font-medium">Render.com</a></p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
