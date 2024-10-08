from dataclasses import dataclass
from time import sleep
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By


BASE_URL = "https://webscraper.io/"
HOME_URL = urljoin(BASE_URL, "test-sites/e-commerce/more/")


URIS = {
    "home": "",
    "computers": "computers",
    "laptops": "computers/laptops",
    "tablets": "computers/tablets",
    "phones": "phones",
    "touch": "phones/touch",
}


@dataclass
class Product:
    title: str
    description: str
    price: float
    rating: int
    num_of_reviews: int


def parse_page(driver: webdriver.Firefox) -> [Product]:
    elements = driver.find_elements(By.CLASS_NAME, "card")
    products = []

    for element in elements:
        title = element.find_element(By.CLASS_NAME, "title").text
        description = element.find_element(By.CLASS_NAME, "description").text
        price = float(
            element.find_element(By.CLASS_NAME, "price").text.replace("$", "")
        )
        rating = len(element.find_elements(By.CLASS_NAME, "ws-icon-star"))
        num_of_reviews = int(
            element.find_element(By.CLASS_NAME, "review-count").text.split()[0]
        )
        products.append(
            Product(title, description, price, rating, num_of_reviews)
        )

    return products


def click_all_more(driver: webdriver.Firefox, uri: str) -> webdriver.Firefox:
    driver.get(urljoin(HOME_URL, uri))
    sleep(1)
    try:
        cookies_btn = driver.find_element(By.CLASS_NAME, "acceptCookies")
        cookies_btn.click()
    except:
        pass

    try:
        more_btn = driver.find_element(
            By.CLASS_NAME, "ecomerce-items-scroll-more"
        )
        while more_btn.is_displayed():
            more_btn.click()

    except:
        pass

    return driver


def get_all_products() -> None:
    with webdriver.Firefox() as driver:

        for page_name, uri in URIS.items():
            page = click_all_more(driver, uri)
            products = parse_page(page)
            print(len(products))

        sleep(5)


if __name__ == "__main__":
    get_all_products()
