from selenium import webdriver
import time
import requests
from selenium.webdriver.common.by import By
import os
import PyPDF2

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

if __name__ == "__main__":
    driver = webdriver.Chrome()

    driver.get("https://dl.acm.org/doi/proceedings/10.1145/3299815")

    time.sleep(5) 

    pdf_links = driver.find_elements(By.CSS_SELECTOR, "a[data-title='PDF']")
    folder = '/Users/yihanping/Documents/gatech/Research/ProcessPDF/pdf_downloads/test_dataset_large/CS/json_forAllMajor'
    n = 0
    m = 10

    for link in pdf_links:
        if m>0:
            pdf_url = link.get_attribute('href')
            response = requests.get(pdf_url)
            if response.status_code == 200:
                os.makedirs(folder, exist_ok=True)
                filename = os.path.join(folder, pdf_url.split('/')[-1])
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded {filename}")
                m = m-1
                if filename:
                    if check_metadata(filename):
                        n += 1
                    else:
                        os.remove(filename)


        else:
            print(f"Failed to download {pdf_url}")


    driver.quit()

