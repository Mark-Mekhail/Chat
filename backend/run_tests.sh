#!/bin/bash
set -e

echo "Running backend tests..."

export ENVIRONMENT=test
export TESTING=true
export MODEL_PATH="/app/models/test-model.gguf"
export MODEL_DIR="/app/models"
export PYTHONPATH=/app

mkdir -p /app/models
if [ ! -f "/app/models/test-model.gguf" ]; then
    echo "Creating test model file"
    echo "Test model file for testing purposes only" > /app/models/test-model.gguf
fi

python -m pytest -v --color=yes

if [ $? -eq 0 ]; then
    echo -e "\n✅ All tests completed successfully! ✅"
else
    echo -e "\n❌ Tests failed! ❌"
    exit 1
fi
python -m pytest -v --color=yes

# Check the exit code
if [ $? -eq 0 ]; then
    echo -e "\n✅ All tests completed successfully! ✅"
else
    echo -e "\n❌ Tests failed! ❌"
    exit 1
fi
