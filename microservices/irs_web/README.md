# IRS Search Engine (Web Interface)

Web interface for the Information Retrieval System (IRS), designed to search Vietnamese articles using semantic search technology.

![IRS Search Preview](/public/og-image.png)

## 🚀 Features

- **Semantic Search**: Intelligent search capabilities for Vietnamese content.
- **Advanced Filtering**: Filter results by category and limit.
- **Search History**: Local storage persistence for recent searches.
- **Responsive Design**: Optimized for Mobile, Tablet, and Desktop.
- **Dark Mode Support**: Adaptive UI for different lighting conditions.
- **SEO Optimized**: Metatags, OpenGraph, and JSON-LD ready.
- **Performance**: Built with Next.js 16 and React Query for optimal speed.

## 🛠 Tech Stack

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS 4
- **UI Components**: Shadcn UI (Radix Primitives)
- **State Management**: Zustand + React Query
- **Animations**: Framer Motion + React Three Fiber (Hero)
- **Form Handling**: React Hook Form + Zod

## 📂 Project Structure

The project follows a **Feature-based Architecture**:

```
irs_web/
├── app/                 # Next.js App Router
├── core/                # Core utilities (HTTP, Env)
├── features/            # Feature modules
│   └── search/          # Search feature (Logic, Components, etc.)
├── components/          # Shared UI components
├── lib/                 # Global utilities
├── store/               # Global state (Zustand)
└── public/              # Static assets
```

## 🏁 Getting Started

### Prerequisites

- Node.js 18+
- pnpm 9+

### Installation

1. Clone the repository:

   ```bash
   git clone <repo-url>
   cd irs_web
   ```

2. Install dependencies:

   ```bash
   pnpm install
   ```

3. Configure Environment Variables:
   Copy `.env.example` to `.env.local`:

   ```bash
   cp .env.example .env.local
   ```

   Update the variables:

   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NEXT_PUBLIC_APP_NAME="IRS Search"
   NEXT_PUBLIC_APP_URL="http://localhost:3000"
   ```

4. Run Development Server:
   ```bash
   pnpm dev
   ```
   Open [http://localhost:3000](http://localhost:3000) to view the app.

## 📦 Deployment

### Vercel (Recommended)

The easiest way to deploy is using Vercel.

1. Push your code to GitHub/GitLab.
2. Import the project in Vercel.
3. Add Environment Variables in Vercel Project Settings.
4. Deploy.

### Docker

Build the container:

```bash
docker build -t irs-web .
```

## 🧪 Testing

Run linting:

```bash
pnpm lint
```

Build for production to verify:

```bash
pnpm build
```

## 📄 License

[MIT](LICENSE)
