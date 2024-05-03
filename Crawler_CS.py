import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

import os
from urllib.parse import urljoin
import PyPDF2

def get_best_paper():
    url = 'https://jeffhuang.com/best_paper_awards/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    best_paper_awards = []

    trs = soup.find_all('tr')
    for tr in trs:
        td = tr.find('td')
        if td is not None:
            a = td.find('a')
            href = a['href']
            print(href)
            print(a.text)
            best_paper_awards.append({'href': href, 'title': a.text})
            print('-------------------')

    print('Total:', len(best_paper_awards))
    return best_paper_awards

def download_pdf(link):
    base_url = 'https://dl.acm.org'
    folder = 'ProcessPDF/pdf_downloads/CSKeywords'
    full_url = urljoin(base_url, link)
    response = requests.get(full_url)
    if response.status_code == 200:
        os.makedirs(folder, exist_ok=True)
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

    links = soup.find('a', {'aria-label': 'PDF'}).get('href')
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
    # best_paper = get_best_paper()
    # find_paper(best_paper)
    url = 'https://dl.acm.org/doi/proceedings/10.1145/986537'
    download_all_pdfs(url)
