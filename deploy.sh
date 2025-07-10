#!/bin/bash

# Deployment script for Koyeb
echo "Starting deployment preparation for Koyeb..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
fi

# Add all files
echo "Adding files to git..."
git add .

# Commit changes
echo "Committing changes..."
git commit -m "Deploy to Koyeb - $(date)"

# Check deployment readiness
echo "Checking deployment readiness..."

# Verify required files exist
required_files=("app.py" "requirements.txt" "Procfile" ".koyeb.yml" "runtime.txt")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file is missing"
        exit 1
    fi
done

# Verify templates directory
if [ -d "templates" ]; then
    echo "✓ templates directory exists"
else
    echo "✗ templates directory is missing"
    exit 1
fi

# Verify static directory
if [ -d "static" ]; then
    echo "✓ static directory exists"
else
    echo "✗ static directory is missing"
    exit 1
fi

echo ""
echo "🚀 Deployment files ready!"
echo ""
echo "Next steps:"
echo "1. Push your code to a Git repository (GitHub, GitLab, etc.)"
echo "2. Connect your repository to Koyeb"
echo "3. Deploy using the .koyeb.yml configuration"
echo "4. Your app will be available at the Koyeb-provided URL"
echo ""
echo "Configuration summary:"
echo "- App name: mysecondweb"
echo "- Port: 8000"
echo "- Health check: /health"
echo "- Instance type: nano"
echo "- Python version: 3.11.9"
echo ""
echo "Deployment preparation complete! ✅"