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

def extract_images(soup, base_url):
    """Extract all image URLs from the page."""
    images = []
    for img in soup.find_all('img', src=True):
        img_url = urljoin(base_url, img['src'])
        images.append(img_url)
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
    url = "https://example.com"  # Replace with your target URL
    page_content = get_page_content(url)
    
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        
        # Extract text content
        text = extract_text(soup)
        print("Text Content:")
        print(text)
        
        # Extract images
        images = extract_images(soup, url)
        print("\nImages:")
        for img in images:
            print(img)
        
        # Extract hyperlinks
        hyperlinks = extract_hyperlinks(soup, url)
        print("\nHyperlinks:")
        for text, link in hyperlinks:
            print(f"Text: {text}, URL: {link}")
        
        # Optionally, get headings of linked pages
        print("\nHeadings of Linked Pages:")
        for text, link in hyperlinks:
            heading = get_heading(link)
            print(f"Link: {link}, Heading: {heading}")

if __name__ == "__main__":
    main()
