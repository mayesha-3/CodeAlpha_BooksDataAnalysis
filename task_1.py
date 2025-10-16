import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://books.toscrape.com/catalogue/category/books/classics_6/"
page_url = "index.html"
books = []

while page_url:
    response = requests.get(base_url + page_url)
    soup = BeautifulSoup(response.text, "html.parser")

    for book in soup.select(".product_pod"):
        title = book.h3.a["title"]
        price = book.select_one(".price_color").text[2:]  # Remove £
        availability = book.select_one(".availability").text.strip()
        rating = book.p["class"][1]  


        books.append({
            "Title": title,
            "Price": float(price),
            "Availability": availability,
            "Rating": rating
        })

    next_btn = soup.select_one(".next > a")
    page_url = next_btn["href"] if next_btn else None

df = pd.DataFrame(books)
df.to_csv("classic_books.csv", index=False)
