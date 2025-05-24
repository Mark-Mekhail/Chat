#!/usr/bin/env bash
# Check for and install required dependencies

# Source utils
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/utils.sh"

check_dependencies() {
  print_message "info" "Checking for required dependencies..."
  
  if is_macos; then
    check_macos_dependencies
  else
    check_install_dependency docker "Docker" "skip" || return 1
    check_install_dependency curl "curl" "skip" || check_install_dependency wget "wget" "skip" || return 1
  fi
  
  # Check if Docker is running
  if command_exists docker; then
    docker info &> /dev/null
    if [ $? -ne 0 ]; then
      print_message "warning" "Docker is installed but not running. Starting Docker..."
      if is_macos; then
        open -a Docker
        print_message "info" "Waiting for Docker to start..."
        sleep 10  # Give Docker time to start
      else
        print_message "error" "Please start Docker manually."
        return 1
      fi
    else
      print_message "success" "Docker is running."
    fi
  fi
  
  check_docker_compose || return 1
  
  return 0
}

check_macos_dependencies() {
  if ! command_exists brew; then
    print_message "warning" "Homebrew is not installed. It's recommended for installing dependencies on macOS."
    print_message "info" "Install Homebrew? (y/n)"
    read -r install_brew
    if [[ "$install_brew" == "y" || "$install_brew" == "Y" ]]; then
      print_message "info" "Installing Homebrew..."
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
      print_message "info" "Skipping Homebrew installation."
    fi
  fi
  
  if command_exists brew; then
    check_install_dependency docker "Docker" "brew install --cask docker" || return 1
    check_install_dependency curl "curl" "brew install curl" || check_install_dependency wget "wget" "brew install wget" || return 1
  else
    check_install_dependency docker "Docker" "skip" || return 1
    check_install_dependency curl "curl" "skip" || check_install_dependency wget "wget" "skip" || return 1
  fi
  
  return 0
}

check_docker_compose() {
  if ! docker compose version &> /dev/null; then
    print_message "warning" "Docker Compose not found as 'docker compose'..."
    
    if command_exists docker-compose; then
      print_message "info" "Found legacy 'docker-compose' command instead."
      # Create an alias or function to use docker-compose instead
      docker() {
        if [ "$1" = "compose" ]; then
          shift
          command docker-compose "$@"
        else
          command docker "$@"
        fi
      }
      export -f docker
    else
      print_message "warning" "Docker Compose not available."
      
      if is_macos; then
        if command_exists brew; then
          print_message "info" "Attempting to install Docker Compose via Homebrew..."
          brew install docker-compose
        else
          print_message "error" "Please install Docker Compose manually."
          print_message "info" "Run: brew install docker-compose"
          return 1
        fi
      else
        if command_exists apt-get; then
          print_message "info" "Attempting to install Docker Compose via apt..."
          sudo apt-get update
          sudo apt-get install -y docker-compose
        elif command_exists yum; then
          print_message "info" "Attempting to install Docker Compose via yum..."
          sudo yum install -y docker-compose
        else
          print_message "error" "Please install Docker Compose manually."
          print_message "info" "Visit: https://docs.docker.com/compose/install/"
          return 1
        fi
      fi
    fi
    
    if ! docker compose version &> /dev/null && ! command_exists docker-compose; then
      print_message "error" "Error: Docker Compose not available. Please install Docker Compose first."
      return 1
    fi
  fi
  
  return 0
}

# Run the dependencies check if this script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  check_dependencies
fi
