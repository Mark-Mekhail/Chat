#!/usr/bin/env bash
# Utility functions for the AI Chat application

# Print colored messages
print_message() {
  local type=$1
  local message=$2
  
  case $type in
    "info")
      echo -e "\033[0;34m[INFO]\033[0m $message"
      ;;
    "success")
      echo -e "\033[0;32m[SUCCESS]\033[0m $message"
      ;;
    "warning")
      echo -e "\033[0;33m[WARNING]\033[0m $message"
      ;;
    "error")
      echo -e "\033[0;31m[ERROR]\033[0m $message"
      ;;
    *)
      echo "$message"
      ;;
  esac
}

command_exists() {
  command -v "$1" &> /dev/null
}

# Check for required tools and install if possible
check_install_dependency() {
  local cmd=$1
  local name=$2
  local install_cmd=$3
  
  if ! command_exists "$cmd"; then
    print_message "warning" "$name is not installed."
    if [[ "$install_cmd" != "skip" ]]; then
      print_message "info" "Attempting to install $name..."
      if eval "$install_cmd"; then
        print_message "success" "$name installed successfully."
      else
        print_message "error" "Failed to install $name. Please install it manually."
        return 1
      fi
    else
      print_message "error" "Please install $name manually."
      return 1
    fi
  else
    print_message "success" "$name is installed."
  fi
  
  return 0
}

# Get the amount of system memory in MB
get_system_memory() {
  local memory_mb
  memory_mb=$(( $(sysctl -n hw.memsize 2>/dev/null || free -m | grep Mem | awk '{print $2}' 2>/dev/null || echo 8000) / 1024 / 1024 ))
  echo "$memory_mb"
}

is_macos() {
  [[ "$(uname)" == "Darwin" ]]
}

is_linux() {
  [[ "$(uname)" == "Linux" ]]
}

ensure_directory() {
  if [ ! -d "$1" ]; then
    print_message "info" "Creating directory: $1"
    mkdir -p "$1"
  fi
}
