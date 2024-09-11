from selenium.webdriver.common.by import By
from selenium import webdriver
from requester import Requester
from book import Book

class Scraper:    
    def __init__(self, website_url: str):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--incognito")
        self.options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=self.options)
        self.requester = Requester(server_url="http://localhost:8080", endpoint="/books")
        self.website_url = website_url

        self.scrape()

    def scrape(self):
        self.driver.get(self.website_url)
        title = self.driver.find_element(By.CLASS_NAME, "product-title").text
        author = self.driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/div/div[1]/div/div[2]/span[1]").text
        year = int(self.driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[8]/td/p").text)
        genre = self.driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div[2]/div/div[1]/div/div[2]/div[6]/span[2]/a").text
        
        description_txt =  self.driver.find_element(By.CLASS_NAME, "livriz-text-synopsis").text
        description = description_txt[0:min(len(description_txt), 255)]
        
        isbn = int(self.driver.find_element(By.CLASS_NAME, "sku").text)
        price: float =  float(self.driver.find_element(By.CLASS_NAME, "product-page-price ").text.replace("$", "").replace(".", "").replace(",", "."))
        genre = "NOVELA"
        book = Book(title, author, year, price, genre, 100, description, isbn)
        self.requester.send_book(book)