import requests
from book import Book

class Requester:
    def __init__(self, server_url: str, endpoint: str):
        self.server_url = server_url
        self.endpoint = endpoint

    def send_book(self, book: Book):
        requests.post(self.server_url + self.endpoint, json=book.__dict__)

    def send_books(self, books: list[Book]):
        for book in books:
            self.send_book(book)