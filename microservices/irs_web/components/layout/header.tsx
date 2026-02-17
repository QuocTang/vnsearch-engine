import Link from "next/link";
import { ThemeToggle } from "./theme-toggle";

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-between">
        <div className="flex items-center gap-2">
          <Link href="/">
            <h1 className="text-xl font-bold">IRS Search</h1>
          </Link>
        </div>

        <div className="flex items-center gap-4">
          <ThemeToggle />
          {/* API Status Indicator */}
          <div className="flex items-center gap-2 text-sm">
            <div className="h-2 w-2 rounded-full bg-green-500" />
            <span className="text-muted-foreground">API Online</span>
          </div>
        </div>
      </div>
    </header>
  );
}
