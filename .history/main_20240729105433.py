import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def sanitize_filename(filename):
    """Sanitize the filename by removing or replacing invalid characters."""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized = ''.join(c for c in filename if c in valid_chars)
    return sanitized.rstrip('.')

def is_image_url(url):
    """Check if the URL points to an image file by checking its extension."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'}
    parsed_url = urlparse(url)
    return os.path.splitext(parsed_url.path)[1].lower() in image_extensions

def extract_images(soup, base_url, folder_path):
    """Extract all image URLs from the page and save the images."""
    images = []
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for img in soup.find_all('img', src=True):
        img_url = urljoin(base_url, img['src'])
        if is_image_url(img_url):
            images.append(img_url)
            try:
                img_data = requests.get(img_url).content
                # Extract the image name and sanitize it
                img_name = os.path.basename(urlparse(img_url).path)
                img_name = sanitize_filename(unquote(img_name))
                img_path = os.path.join(folder_path, img_name)
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data)
                print(f"Saved {img_path}")
            except Exception as e:
                print(f"Could not save image {img_url}: {e}")
    return images

def get_page_content_selenium(url):
    """Fetch the content of the web page using Selenium."""
    options = Options()
    options.headless = True
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    # Replace with the path to your chromedriver executable
    service = Service('C:/path/to/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        return driver.page_source
    finally:
        driver.quit()

def extract_text(soup):
    """Extract and return the main text content of the page."""
    return soup.get_text(separator=' ', strip=True)

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
        content = get_page_content_selenium(url)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            heading = soup.title.string if soup.title else "No Title"
            return heading
    except Exception as e:
        print(f"Error fetching heading for URL {url}: {e}")
    return "No Title"

def main():
    url = "https://pwskills.com"  # Replace with your target URL
    content = get_page_content_selenium(url)
    
    if content:
        soup = BeautifulSoup(content, 'html.parser')
    
        text = extract_text(soup)
        print("Text Content:")
        print(text)
        
        # Directory to save images
        images_folder = "fetched_images"
        images = extract_images(soup, url, images_folder)
        if images:
            print("\nImages:")
            for img in images:
                print(img)
        else:
            print("\nNo images found.")
        
        hyperlinks = extract_hyperlinks(soup, url)
        if hyperlinks:
            print("\nHyperlinks:")
            for text, link in hyperlinks:
                print(f"Text: {text}, URL: {link}")
            
            print("\nHeadings of Linked Pages:")
            for text, link in hyperlinks:
                heading = get_heading(link)
                print(f"Link: {link}, Heading: {heading}")
        else:
            print("\nNo hyperlinks found.")
    else:
        print("Failed to retrieve content from the URL.")

if __name__ == "__main__":
    main()
