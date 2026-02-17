/**
 * Environment Configuration
 * Centralized env variables với validation và fallback
 */

const getEnvVar = (key: string, fallback?: string): string => {
  const value = process.env[key];

  if (!value) {
    if (fallback !== undefined) {
      console.warn(
        `Environment variable ${key} not set, using fallback: ${fallback}`,
      );
      return fallback;
    }
    throw new Error(`Missing required environment variable: ${key}`);
  }

  return value;
};

export const environment = {
  API_BASE_URL: getEnvVar(
    "NEXT_PUBLIC_API_BASE_URL",
    "http://localhost:8000", // Fallback for development
  ),
  APP_NAME: getEnvVar("NEXT_PUBLIC_APP_NAME", "IRS Search"),
  APP_URL: getEnvVar("NEXT_PUBLIC_APP_URL", "http://localhost:3000"),
  IS_PRODUCTION: process.env.NODE_ENV === "production",
  IS_DEVELOPMENT: process.env.NODE_ENV === "development",
} as const;
