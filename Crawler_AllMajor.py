import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import PyPDF2

def download_pdf(link):
    base_url = 'https://biomedical-engineering-online.biomedcentral.com'
    folder = 'ProcessPDF/pdf_downloads/test_dataset/AllMajor'
    full_url = urljoin(base_url, link)
    response = requests.get(full_url)
    if response.status_code == 200:
        # Create download folder if it doesn't exist
        os.makedirs(folder, exist_ok=True)
        # Extract filename and create full path
        filename = os.path.join(folder, link.split('/')[-1])
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
        return filename
    else:
        print(f"Failed to download {link}")
        return None

def check_metadata(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        metadata = pdf_reader.metadata
        # Cleaning up metadata (some values can be in a different format)
        cleaned_metadata = {key: (value if isinstance(value, str) else str(value)) for key, value in metadata.items()}
        if '/Keywords' in cleaned_metadata and cleaned_metadata['/Keywords']:
            print(cleaned_metadata['/Keywords'])
            return True
        else:
            return False

def download_all_pdfs(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)
    n = 0
    for link in links:
        if n > 50:
            break
        href = link['href']
        if href.endswith('.pdf'):
            filepath = download_pdf(href)
            if filepath:
                if check_metadata(filepath):
                    n += 1
                else:
                    os.remove(filepath)

if __name__ == "__main__":
    # url = 'https://bmcchem.biomedcentral.com/articles'
    url = 'https://biomedical-engineering-online.biomedcentral.com/articles'
    download_all_pdfs(url)
