-- Create n8n database and user
-- This script runs automatically when PostgreSQL container starts

-- Create n8n user
CREATE USER n8n WITH PASSWORD 'n8n';

-- Create n8n database
CREATE DATABASE n8n WITH OWNER n8n;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE n8n TO n8n;

-- Connect to n8n database and set schema permissions
\c n8n
GRANT ALL PRIVILEGES ON SCHEMA public TO n8n;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO n8n;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO n8n;
