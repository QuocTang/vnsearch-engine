export function Footer() {
  return (
    <footer className="border-t">
      <div className="container mx-auto flex h-16 items-center justify-center py-4">
        <p className="text-sm text-muted-foreground">
          © 2026 IRS Search. Powered by FastAPI + Qdrant + Next.js
        </p>

        {/* <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <a href="/docs" className="hover:text-foreground">
            API Docs
          </a>
          <a href="/about" className="hover:text-foreground">
            About
          </a>
        </div> */}
      </div>
    </footer>
  );
}
