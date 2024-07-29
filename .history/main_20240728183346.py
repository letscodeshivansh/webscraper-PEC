import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_page_content(url):
    """Fetch the content of the web page."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def extract_text(soup):
    """Extract and return the main text content of the page."""
    text = soup.get_text(separator=' ', strip=True)
    return text
    
def extract_images(soup, base_url, folder_path):
    """Extract all image URLs from the page and save the images."""
    images = []
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for img in soup.find_all('img', src=True):
        img_url = urljoin(base_url, img['src'])
        images.append(img_url)
        try:
            img_data = requests.get(img_url).content
            # Extract the image name and sanitize it
            img_name = os.path.basename(urlparse(img_url).path)
            img_name = sanitize_filename(img_name)
            img_path = os.path.join(folder_path, img_name)
            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)
            print(f"Saved {img_path}")
        except Exception as e:
            print(f"Could not save image {img_url}: {e}")
    return images

def extract_hyperlinks(soup, base_url):
    """Extract all hyperlinks and their texts from the page."""
    hyperlinks = []
    for a_tag in soup.find_all('a', href=True):
        href = urljoin(base_url, a_tag['href'])
        text = a_tag.get_text(strip=True)
        hyperlinks.append((text, href))
    return hyperlinks

def get_heading(url):
    """Fetch the heading of a linked page."""
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
    url = "https://ndtv.com"  # Replace with your target URL
    content = get_page_content(url)
    
    if content:
        soup = BeautifulSoup(content, 'html.parser')
    
        text = extract_text(soup)
        print("Text Content:")
        print(text)
        
        # Directory to save images
        images_folder = "fetched_images"
        images = extract_images(soup, url, images_folder)
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
