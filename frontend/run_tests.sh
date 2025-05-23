#!/bin/bash
set -e

docker build -t chatbot-frontend-test -f Dockerfile.test .
docker run --rm chatbot-frontend-test
