#!/bin/bash
set -e

docker build -t chatbot-backend-test -f Dockerfile.test .
docker run --rm chatbot-backend-test