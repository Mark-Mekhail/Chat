#!/usr/bin/env bash
# Main script to start the AI Chat application

# Set errexit, nounset, pipefail options for better error handling
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SCRIPTS_DIR="$PROJECT_ROOT/scripts"

source "$SCRIPTS_DIR/utils.sh"

main() {
  print_message "info" "Starting AI Chat application setup..."
  
  print_message "info" "Checking system dependencies..."
  source "$SCRIPTS_DIR/check_dependencies.sh"
  if ! check_dependencies; then
    print_message "error" "Failed to verify required dependencies."
    exit 1
  fi
  
  print_message "info" "Checking for AI model..."
  source "$SCRIPTS_DIR/model_manager.sh"
  if ! check_and_download_model; then
    print_message "error" "Failed to set up model. Cannot continue."
    exit 1
  fi
  
  print_message "info" "Starting Docker containers..."
  source "$SCRIPTS_DIR/docker_manager.sh"
  if ! start_application; then
    print_message "error" "Failed to start the application."
    exit 1
  fi
  
  print_message "success" "Setup completed successfully."
  return 0
}

usage() {
  cat << EOF
    Usage: app.sh [COMMAND]

    Commands:
    run      Start the application
    stop     Stop the application
    restart  Restart the application
    logs     Show application logs
    status   Check application status
    model    Check or download the model
    help     Show this help message (default if no command is provided)

EOF
}

# Parse command line arguments
if [ $# -eq 0 ]; then
  # No arguments, run help function
  usage
else
  case "$1" in
    start)
      main
      ;;
    stop)
      source "$SCRIPTS_DIR/docker_manager.sh"
      stop_application
      ;;
    restart)
      source "$SCRIPTS_DIR/docker_manager.sh"
      stop_application && start_application
      ;;
    logs)
      source "$SCRIPTS_DIR/docker_manager.sh"
      show_logs
      ;;
    status)
      source "$SCRIPTS_DIR/docker_manager.sh"
      check_application_status
      ;;
    model)
      source "$SCRIPTS_DIR/model_manager.sh"
      check_and_download_model
      ;;
    help)
      usage
      ;;
    *)
      print_message "error" "Unknown command: $1"
      usage
      exit 1
      ;;
  esac
fi

exit 0
