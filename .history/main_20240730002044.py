import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import hashlib

def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def extract_text(soup):
    text = soup.get_text(separator=' ', strip=True)
    return text

def save_image(image_url, directory):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        
        # Create a hash of the image URL to use as the filename
        image_hash = hashlib.md5(image_url.encode('utf-8')).hexdigest()
        image_name = f"{image_hash}.jpg"
        
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)
        image_path = os.path.join(directory, image_name)

        with open(image_path, 'wb') as f:
            f.write(response.content)
        print(f"Saved image: {image_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image {image_url}: {e}")

def extract_images(soup, base_url, directory="fetched_images"):
    # Check if the path exists and is not a directory
    if os.path.exists(directory) and not os.path.isdir(directory):
        # If it is a file, create a new directory with a unique name
        directory = f"{directory}_new"
    
    images = []
    for img in soup.find_all('img', src=True):
        img_url = urljoin(base_url, img['src'])
        images.append(img_url)
        save_image(img_url, directory)  # Save each image
    return images

def extract_hyperlinks(soup, base_url):
    hyperlinks = []
    for a_tag in soup.find_all('a', href=True):
        href = urljoin(base_url, a_tag['href'])
        text = a_tag.get_text(strip=True)
        hyperlinks.append((text, href))
    return hyperlinks

def get_heading(url):
    try:
        content = get_page_content(url)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            heading = soup.title.string if soup.title else "No Title"
            return heading
    except Exception as e:
        print(f"Error fetching heading for URL {url}: {e}")
    return "No Title"

def main():
    url = "https://.com"  
    content = get_page_content(url)
    
    if content:
        soup = BeautifulSoup(content, 'html.parser')
    
        text = extract_text(soup)
        print("Text Content:")
        print(text)
        
        images = extract_images(soup, url)
        print("\nImages:")
        for img in images:
            print(img)
        
        hyperlinks = extract_hyperlinks(soup, url)
        print("\nHyperlinks:")
        for text, link in hyperlinks:
            print(f"Text: {text}, URL: {link}")
        
        print("\nHeadings of Linked Pages:")
        for text, link in hyperlinks:
            heading = get_heading(link)
            print(f"Link: {link}, Heading: {heading}")
    else: 
        print("URL is not correct")

if __name__ == "__main__":
    main()
