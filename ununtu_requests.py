import requests
import os
from urllib.parse import urlparse
import hashlib

def fetch_images(urls):
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Create directory if it doesn't exist
    os.makedirs("Fetched_Images", exist_ok=True)

    for url in urls:
        url = url.strip()
        if not url:
            continue

        try:
            # Fetch the image with headers only (HEAD request first for safety)
            head_response = requests.head(url, timeout=10, allow_redirects=True)
            head_response.raise_for_status()

            # Check important headers
            content_type = head_response.headers.get("Content-Type", "")
            content_length = head_response.headers.get("Content-Length")

            # Precaution: ensure it's an image
            if not content_type.startswith("image/"):
                print(f"✗ Skipped (not an image): {url}")
                continue

            # Download the actual content
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Extract filename from URL or generate one
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)

            if not filename:
                filename = "downloaded_image.jpg"

            filepath = os.path.join("Fetched_Images", filename)

            # Prevent duplicates by checking file hash
            file_hash = hashlib.sha256(response.content).hexdigest()
            duplicate_found = False

            for existing_file in os.listdir("Fetched_Images"):
                existing_path = os.path.join("Fetched_Images", existing_file)
                with open(existing_path, "rb") as f:
                    existing_hash = hashlib.sha256(f.read()).hexdigest()
                if existing_hash == file_hash:
                    print(f"✗ Duplicate skipped: {filename}")
                    duplicate_found = True
                    break

            if duplicate_found:
                continue

            # Save image
            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"✓ Successfully fetched: {filename}")
            print(f"✓ Image saved to {filepath}")

            if content_length:
                print(f"ℹ File size: {int(content_length)/1024:.2f} KB")

        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error: {e}")
        except Exception as e:
            print(f"✗ An unexpected error occurred: {e}")

    print("\nConnection strengthened. Community enriched.")

def main():
    # Get multiple URLs from user (comma-separated)
    urls_input = input("Please enter one or more image URLs (comma-separated):\n")
    urls = urls_input.split(",")
    fetch_images(urls)

if __name__ == "__main__":
    main()

