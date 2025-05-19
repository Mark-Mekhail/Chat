#!/usr/bin/env python3
"""
Script to download a compatible LLM model for the AI Chat app.
"""

import os
import sys
import argparse
import requests
from tqdm import tqdm

DEFAULT_MODEL_URL = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
DEFAULT_OUTPUT_DIR = "models"
DEFAULT_FILENAME = "llama-2-7b-chat.gguf"

def download_file(url, output_path, force=False, non_interactive=False):
    """
    Download a file with progress bar
    
    Args:
        url: URL to download from
        output_path: Path to save the file
        force: Force download even if file exists
        non_interactive: If True, won't prompt for input
    
    Returns:
        bool: True if download succeeded or file exists, False otherwise
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Check if file already exists
    if os.path.exists(output_path) and not force:
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"File already exists at {output_path} ({size_mb:.2f} MB)")
        
        if non_interactive:
            print("Using existing model file.")
            return True
        
        choice = input("Do you want to re-download it? (y/n): ").lower()
        if choice != 'y':
            print("Using existing model file.")
            return True
    
    # Start the download
    try:
        print(f"Downloading model from {url}")
        print(f"This might take several minutes depending on your internet speed.")
        print(f"Target location: {output_path}")
        
        # Use a session for better performance
        session = requests.Session()
        response = session.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        total_size = int(response.headers.get('content-length', 0))
        
        # Show progress bar
        with open(output_path, 'wb') as file, tqdm(
            desc=os.path.basename(output_path),
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=8192):
                size = file.write(data)
                bar.update(size)
        
        # Verify the download
        if os.path.exists(output_path):
            actual_size = os.path.getsize(output_path)
            if total_size > 0 and abs(actual_size - total_size) > 1024:  # Allow 1KB difference
                print(f"Warning: File size mismatch. Expected {total_size} bytes, got {actual_size} bytes.")
                return False
                
        print(f"Download complete. Model saved to {output_path}")
        return True
        
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Download LLM model for AI Chat")
    parser.add_argument(
        "--url", 
        default=DEFAULT_MODEL_URL,
        help=f"URL to download the model from (default: {DEFAULT_MODEL_URL})"
    )
    parser.add_argument(
        "--output-dir", 
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to save the model to (default: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        "--filename", 
        default=DEFAULT_FILENAME,
        help=f"Filename to save the model as (default: {DEFAULT_FILENAME})"
    )
    parser.add_argument(
        "--force", 
        action="store_true",
        help="Force download even if the file already exists"
    )
    parser.add_argument(
        "--non-interactive", 
        action="store_true",
        help="Run in non-interactive mode (no prompts)"
    )
    parser.add_argument(
        "--smaller-model", 
        action="store_true",
        help="Download a smaller model variant (useful for systems with limited resources)"
    )
    
    args = parser.parse_args()
    
    # Use a smaller model if requested
    url = args.url
    if args.smaller_model:
        # Use a smaller 3B model instead of 7B
        url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q2_K.gguf"
        print("Using smaller model variant for limited resources.")
    
    output_path = os.path.join(args.output_dir, args.filename)
    success = download_file(url, output_path, args.force, args.non_interactive)
    
    if not success:
        print("Failed to download the model.")
        sys.exit(1)
    
    print("Model is ready to use!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
