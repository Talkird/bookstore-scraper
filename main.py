from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import requests
import json
import time
import sys

class Book:
    def __init__(self, title: str, author: str, year: int, price: float, genre: str, stock: int, description: str, isbn: int):
        self.title = title
        self.author = author
        self.year = year
        self.price = price
        self.genre = genre
        self.stock = stock
        self.isbn = isbn
        self.description = description

class Requester:
    def __init__(self, server_url: str):
        self.server_url = server_url

    def send_book(self, book: Book):
        requests.post(self.server_url, json=book.__dict__)

    def send_books(self, books: list[Book]):
        for book in books:
            self.send_book(book)

class Scraper:    
    def __init__(self, website_url: str):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--incognito")
        self.options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=self.options)
        self.website_url = website_url

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
        requester.send_book(book)

if __name__ == "__main__":
    requester = Requester("http://localhost:8080/books")
    scraper = Scraper("https://cuspide.com/producto/espiritu-animal/")
    scraper.scrape()

