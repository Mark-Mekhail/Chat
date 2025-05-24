#!/usr/bin/env bash
# Handle Docker operations for the application

# Source utils
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/utils.sh"

start_application() {
  cd "$SCRIPT_DIR/.." || return 1
  
  print_message "info" "Pulling latest Docker images..."
  docker compose pull
  
  print_message "info" "Starting AI Chat application..."
  docker compose up -d --build
  
  check_application_status
  return $?
}

check_application_status() {
  build_success=$(docker compose ps | grep -c "ai-chat")
  if [ "$build_success" -eq 0 ]; then
    handle_build_failure
    return $?
  fi
  
  print_message "info" "Checking if services are running..."
  max_attempts=5
  attempt=1
  
  while [ $attempt -le $max_attempts ]; do
    print_message "info" "Attempt $attempt of $max_attempts..."
    
    if docker container ls | grep -q "ai-chat-backend" && docker container ls | grep -q "ai-chat-frontend"; then
      print_message "success" "AI Chat application is running successfully!"
      print_message "info" "You can access it at http://localhost:80"
      print_message "info" ""
      print_message "info" "To view logs: docker compose logs -f"
      print_message "info" "To stop the application: docker compose down"
      
      if command_exists open; then
        print_message "info" "Opening app in browser..."
        open http://localhost:80
      fi
      
      return 0
    fi
    
    print_message "info" "Services not fully running yet. Waiting..."
    sleep 3
    ((attempt++))
  done
  
  print_message "error" "Failed to detect running application properly, but containers may still be running."
  print_message "info" "Checking container status:"
  docker container ls | grep "ai-chat"
  print_message "info" ""
  print_message "info" "Checking logs:"
  docker compose logs --tail=10
  
  return 1
}

handle_build_failure() {
  print_message "warning" "Build may have failed. Checking logs..."
  docker compose logs frontend
  
  print_message "info" "Would you like to view detailed build logs? (y/n)"
  read -r view_logs
  if [[ "$view_logs" == "y" || "$view_logs" == "Y" ]]; then
    docker compose logs --tail=100 frontend
  fi
  
  print_message "info" "Would you like to try building again? (y/n)"
  read -r rebuild
  if [[ "$rebuild" == "y" || "$rebuild" == "Y" ]]; then
    print_message "info" "Rebuilding frontend container..."
    docker compose build frontend
    docker compose up -d
    return 0
  fi
  
  return 1
}

stop_application() {
  print_message "info" "Stopping AI Chat application..."
  docker compose down
  
  if [ $? -eq 0 ]; then
    print_message "success" "Application stopped successfully."
  else
    print_message "error" "Failed to stop the application."
    return 1
  fi
  
  return 0
}

show_logs() {
  print_message "info" "Showing application logs (press Ctrl+C to exit)..."
  docker compose logs -f
}

# Run the docker operations if this script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  # If no arguments provided, start the application
  if [ $# -eq 0 ]; then
    start_application
  else
    case "$1" in
      start)
        start_application
        ;;
      stop)
        stop_application
        ;;
      restart)
        stop_application && start_application
        ;;
      logs)
        show_logs
        ;;
      status)
        check_application_status
        ;;
      *)
        print_message "error" "Unknown command: $1"
        print_message "info" "Usage: docker_manager.sh [start|stop|restart|logs|status]"
        exit 1
        ;;
    esac
  fi
fi
