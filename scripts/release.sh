#!/bin/bash

# Manual release script for CLIck
# Usage: ./scripts/release.sh [patch|minor|major]

set -e

BUMP_TYPE=${1:-patch}

echo "🚀 Creating $BUMP_TYPE release..."

# Ensure we're on master/main branch
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" != "master" && "$CURRENT_BRANCH" != "main" ]]; then
    echo "❌ Must be on master or main branch. Currently on: $CURRENT_BRANCH"
    exit 1
fi

# Ensure working directory is clean
if [[ -n $(git status --porcelain) ]]; then
    echo "❌ Working directory is not clean. Please commit or stash changes."
    exit 1
fi

# Run tests
echo "🧪 Running tests..."
python -m pytest tests/ -v

# Run quality checks
echo "🔍 Running quality checks..."
black --check src/ tests/
mypy src/ --ignore-missing-imports

echo "✅ All checks passed!"

# Create commit with conventional commit message
case $BUMP_TYPE in
    major)
        COMMIT_MSG="feat!: major release with breaking changes"
        ;;
    minor)
        COMMIT_MSG="feat: add new features"
        ;;
    patch)
        COMMIT_MSG="fix: bug fixes and improvements"
        ;;
    *)
        echo "❌ Invalid bump type. Use: patch, minor, or major"
        exit 1
        ;;
esac

# Create empty commit to trigger release
git commit --allow-empty -m "$COMMIT_MSG"
git push origin $CURRENT_BRANCH

echo "🎉 Release triggered! Check GitHub Actions for progress."
echo "📦 Release will be available at: https://github.com/arsovskidev/CLIck/releases"
