#!/bin/bash
# filepath: /Users/Markm/Repos/Projects/Chatbot/run_backend_tests.sh
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="${SCRIPT_DIR}/backend"

# Create test results directory if it doesn't exist
mkdir -p "${SCRIPT_DIR}/test-results"

echo "🧪 Running backend tests in Docker..."

# Check if specific test files were specified
if [ $# -gt 0 ]; then
  echo "Running specific tests: $@"
  docker-compose run --rm backend-test python -m pytest "$@" -v
else
  # Either run using docker-compose or the backend script
  if [ "$USE_COMPOSE" = "true" ]; then
    # Run tests using docker-compose (rebuilds if needed)
    docker-compose run --rm backend-test
  else
    # Navigate to the backend directory and use the dedicated script
    cd "${BACKEND_DIR}"
    ./run_docker_tests.sh
  fi
fi

# Check exit status
if [ $? -eq 0 ]; then
  echo -e "\n✅ All tests passed successfully! ✅"
else
  echo -e "\n❌ Some tests failed! ❌"
  exit 1
fi
