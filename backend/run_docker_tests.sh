#!/bin/bash
# filepath: /Users/Markm/Repos/Projects/Chatbot/backend/run_docker_tests.sh
set -e

echo "Building the test Docker image..."
docker build -t chatbot-backend-test -f Dockerfile.test .

echo "Running tests inside Docker container..."
# We don't need to mount the models volume for tests
docker run --rm chatbot-backend-test

echo "Docker test run complete!"
