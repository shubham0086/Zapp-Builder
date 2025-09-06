-- Content Creator Studio Database Schema
-- PostgreSQL with pgvector extension for vector storage

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    plan_type VARCHAR(50) DEFAULT 'free',
    credits_remaining INTEGER DEFAULT 100,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    topic TEXT NOT NULL,
    tone VARCHAR(100) NOT NULL,
    platforms TEXT[] NOT NULL,
    status VARCHAR(50) DEFAULT 'processing',
    workflow_steps TEXT[] DEFAULT '{}',
    results JSONB,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Research results table with vector storage
CREATE TABLE IF NOT EXISTS research_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    source_url VARCHAR(500),
    title TEXT,
    content TEXT,
    summary TEXT,
    relevance_score FLOAT DEFAULT 0.0,
    embedding vector(1536), -- OpenAI embeddings dimension
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Leads table
CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    platform VARCHAR(100) NOT NULL,
    profile_url VARCHAR(500),
    email VARCHAR(255),
    follower_count INTEGER DEFAULT 0,
    engagement_rate FLOAT DEFAULT 0.0,
    relevance_score FLOAT DEFAULT 0.0,
    bio TEXT,
    tags TEXT[],
    contact_info JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Content drafts table
CREATE TABLE IF NOT EXISTS content_drafts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    platform VARCHAR(100) NOT NULL,
    content_type VARCHAR(100) DEFAULT 'post',
    title VARCHAR(500),
    content TEXT NOT NULL,
    hashtags TEXT[],
    word_count INTEGER,
    estimated_reach INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Outreach messages table
CREATE TABLE IF NOT EXISTS outreach_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
    subject_line VARCHAR(500),
    message_body TEXT NOT NULL,
    platform VARCHAR(100),
    outreach_type VARCHAR(100) DEFAULT 'collaboration',
    estimated_response_rate FLOAT DEFAULT 0.0,
    status VARCHAR(50) DEFAULT 'draft',
    sent_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Brand voice profiles
CREATE TABLE IF NOT EXISTS brand_voice_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    tone_characteristics JSONB,
    example_content TEXT[],
    keywords TEXT[],
    is_default BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- API usage tracking
CREATE TABLE IF NOT EXISTS api_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    endpoint VARCHAR(255) NOT NULL,
    request_data JSONB,
    response_status INTEGER,
    tokens_used INTEGER DEFAULT 0,
    credits_consumed INTEGER DEFAULT 1,
    processing_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Workflow executions for monitoring
CREATE TABLE IF NOT EXISTS workflow_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    workflow_type VARCHAR(100) NOT NULL,
    agent_name VARCHAR(100),
    status VARCHAR(50) DEFAULT 'running',
    start_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    end_time TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    execution_log JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_projects_user_id ON projects(user_id);
CREATE INDEX IF NOT EXISTS idx_projects_created_at ON projects(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);

CREATE INDEX IF NOT EXISTS idx_research_project_id ON research_results(project_id);
CREATE INDEX IF NOT EXISTS idx_research_relevance ON research_results(relevance_score DESC);

CREATE INDEX IF NOT EXISTS idx_leads_project_id ON leads(project_id);
CREATE INDEX IF NOT EXISTS idx_leads_platform ON leads(platform);
CREATE INDEX IF NOT EXISTS idx_leads_relevance ON leads(relevance_score DESC);

CREATE INDEX IF NOT EXISTS idx_content_project_id ON content_drafts(project_id);
CREATE INDEX IF NOT EXISTS idx_content_platform ON content_drafts(platform);

CREATE INDEX IF NOT EXISTS idx_outreach_project_id ON outreach_messages(project_id);
CREATE INDEX IF NOT EXISTS idx_outreach_lead_id ON outreach_messages(lead_id);
CREATE INDEX IF NOT EXISTS idx_outreach_status ON outreach_messages(status);

CREATE INDEX IF NOT EXISTS idx_brand_voice_user_id ON brand_voice_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_brand_voice_default ON brand_voice_profiles(is_default);

CREATE INDEX IF NOT EXISTS idx_api_usage_user_id ON api_usage(user_id);
CREATE INDEX IF NOT EXISTS idx_api_usage_created_at ON api_usage(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_workflow_project_id ON workflow_executions(project_id);
CREATE INDEX IF NOT EXISTS idx_workflow_status ON workflow_executions(status);

-- Vector similarity search index (for research results)
CREATE INDEX IF NOT EXISTS idx_research_embedding ON research_results USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Insert sample data for development
INSERT INTO users (email, hashed_password, plan_type, credits_remaining) VALUES 
('demo@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3QJjABCEfa', 'free', 100),
('admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3QJjABCEfa', 'pro', 1000)
ON CONFLICT (email) DO NOTHING;

-- Sample brand voice profile
INSERT INTO brand_voice_profiles (user_id, name, description, tone_characteristics, example_content, keywords, is_default)
SELECT 
    u.id,
    'Professional Tech Expert',
    'Authoritative yet approachable voice for technology content',
    '{"tone": "professional", "style": "educational", "personality": "expert"}',
    ARRAY['Leveraging AI to transform business operations...', 'The future of technology lies in...'],
    ARRAY['innovation', 'technology', 'AI', 'digital transformation'],
    true
FROM users u WHERE u.email = 'demo@example.com'
ON CONFLICT DO NOTHING;

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers to update updated_at automatically
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_brand_voice_updated_at BEFORE UPDATE ON brand_voice_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_app_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_app_user;