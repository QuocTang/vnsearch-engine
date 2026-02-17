"use client";

import { Suspense } from "react";
import { SearchFeature } from "@/features/search";

/**
 * Home Page - IRS Search
 */
export default function Home() {
  return (
    <div className="container py-8">
      <Suspense fallback={<div>Loading...</div>}>
        <SearchFeature />
      </Suspense>
    </div>
  );
}
