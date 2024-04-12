from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm
import requests
import os
import time
import re
from os import listdir
from os.path import isfile, join
import json

class Web_scraper: 

    def __init__(self, url, browser):
        self.url = url
        if browser.lower() == 'chrome':
            self.driver = webdriver.Chrome()  # For Chrome
        elif browser.lower() == 'firefox':
            self.driver = webdriver.Firefox()  # For Firefox
        elif browser.lower() == 'edge':
            self.driver = webdriver.Edge()  # For Edge
        elif browser.lower() == 'safari':
            self.driver = webdriver.Safari()  # For Safari
        else:
            raise ValueError("Unsupported browser type. Please choose from 'chrome', 'firefox', 'edge', or 'safari'.")
        
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive'}
        
    def get_images(self, scrolls):
        self.driver.get(self.url)
        # Auto-scroll to the bottom of the page to load more images
        
        scroll_count = 0
        while scroll_count < scrolls:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            scroll_count += 1
            print(f"Scroll count: {scroll_count}")

        # Parse the HTML content after auto-scrolling
        bs = BeautifulSoup(self.driver.page_source, 'html.parser')

        # Extract all img tags with class img
        images = bs.find_all('img', attrs={'class':'tile-image lazyload'})
        print(images[0])

        links = [listing['data-srcset'].split(' ')[0].strip() for listing in images]
        print(links[0])
        
        title = [listing['title'] for listing in images]

        return links, title

    def download_images(self, links, title):
        count = 0

        if not os.path.exists('images'):
            os.makedirs('images')
        
        print(f"Total links: {len(links)}, Total titles: {len(title)}")  # Debugging line
        
        for i in tqdm(range(len(links))):
            if i >= len(title):
                print(f"Index {i} out of range for titles list.")  # Debugging line
                break

            cleaned_title = re.sub(r'[\\/*?:"<>|]', '', title[i])
            if not os.path.exists(f'images/{cleaned_title}.jpg'):
                with open(f'images/{cleaned_title}.jpg', 'wb') as f:
                    f.write(requests.get(links[i]).content)
                    count += 1
                    time.sleep(1)
            if count == 250:
                break

        print(f'{count} images downloaded successfully')

    def close_driver(self):
        self.driver.quit()
    
    @staticmethod
    def get_metadata(path):
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))] 
        captions = [file_name.split(".")[0] for file_name in onlyfiles]
        
        l = []
        for i in range(len(onlyfiles)):
            meta = {}
            meta['file_name'] = str(onlyfiles[i])
            meta['text'] = str(captions[i])
            l.append(meta)

        if not os.path.exists(path + "/metadata.jsonl"):
            with open(path + "/metadata.jsonl", 'w') as f:
                for item in l:
                    f.write(json.dumps(item) + "\n")