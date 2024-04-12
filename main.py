from src.web_scraping import Web_scraper
from datasets import load_dataset 
from src.model import ImageCaptioningModel
from src.data_loader import ImageCaptioningDataset
from src.model import Transformer_model
from src.dataset_downloader import CreateImageDataset

if __name__ == "__main__": 

    # url = 'https://www.carrefour.it/spesa-online/dolci-e-prima-colazione/'

    # browser = "Firefox"
    # web_scraper = Web_scraper(url, browser)
    # links, title = web_scraper.get_images(20)
    # web_scraper.download_images(links, title)
    # web_scraper.driver.quit()

    CreateImageDataset().download_images()

   
