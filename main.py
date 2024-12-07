import os
import requests
from bs4 import BeautifulSoup

# Define the URL of the website and the output folder
website_url = "https://example.com"  # Replace with the target website URL
output_folder = "./images"  # Directory to save the image

# Define the image name or partial URL to search for
image_keyword = "specific_image_name_or_partial_url"  # Replace with a specific identifier

def download_image(image_url, save_path):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image downloaded: {save_path}")
    except Exception as e:
        print(f"Failed to download image: {e}")

def main():
    try:
        # Get the webpage content
        response = requests.get(website_url)
        response.raise_for_status()

        # Parse the webpage content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the specific image
        image_tag = None
        for img in soup.find_all('img'):
            if image_keyword in img.get('src', ''):
                image_tag = img
                break

        if not image_tag:
            print("Image not found!")
            return

        # Get the full image URL
        image_url = image_tag['src']
        if not image_url.startswith("http"):
            # Handle relative URLs
            image_url = requests.compat.urljoin(website_url, image_url)

        print(f"Found image URL: {image_url}")

        # Prepare the output directory
        os.makedirs(output_folder, exist_ok=True)
        save_path = os.path.join(output_folder, os.path.basename(image_url))

        # Download the image
        download_image(image_url, save_path)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
