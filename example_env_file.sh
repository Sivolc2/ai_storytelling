#!/bin/bash
# Example environment file for My Adventure Tale
# Copy this to repo_src/backend/.env and fill in your actual API key

# To get a Google API key for Gemini:
# 1. Go to https://makersuite.google.com/app/apikey
# 2. Create a new API key
# 3. Copy the key and paste it below (remove the quotes)

# Replace YOUR_ACTUAL_API_KEY_HERE with your real Google API key
GOOGLE_API_KEY="YOUR_ACTUAL_API_KEY_HERE"

# Database configuration (already set by setup-env.sh)
DATABASE_URL=sqlite:///./app.db

# API settings (already set by setup-env.sh)
PORT=8000
LOG_LEVEL=info 