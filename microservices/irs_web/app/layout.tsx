import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Providers } from "../core/providers/react-query.provider";
import { Header } from "@/components/layout/header";
import { Footer } from "@/components/layout/footer";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

import { environment } from "@/core/environment";

export const metadata: Metadata = {
  metadataBase: new URL(environment.APP_URL),
  title: {
    default: environment.APP_NAME,
    template: `%s | ${environment.APP_NAME}`,
  },
  description:
    "Hệ thống tìm kiếm bài viết tiếng Việt thông minh sử dụng công nghệ Semantic Search.",
  keywords: ["Search Engine", "Semantic Search", "Vietnamese", "NLP", "AI"],
  authors: [{ name: "IRS Team" }],
  creator: "IRS Team",
  openGraph: {
    type: "website",
    locale: "vi_VN",
    url: environment.APP_URL,
    title: environment.APP_NAME,
    description: "Hệ thống tìm kiếm bài viết tiếng Việt thông minh.",
    siteName: environment.APP_NAME,
    images: [
      {
        url: "/og-image.png", // Next.js automatically looks for opengraph-image.png/jpg in app/
        width: 1200,
        height: 630,
        alt: environment.APP_NAME,
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: environment.APP_NAME,
    description: "Hệ thống tìm kiếm bài viết tiếng Việt thông minh.",
    images: ["/og-image.png"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="vi">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Providers>
          <div className="flex min-h-screen flex-col">
            <Header />
            <main className="flex-1 container mx-auto px-4">{children}</main>
            <Footer />
          </div>
        </Providers>
      </body>
    </html>
  );
}
