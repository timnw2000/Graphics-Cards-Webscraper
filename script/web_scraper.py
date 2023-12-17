import requests
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet

import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os
import re
import threading

import whatsapp_operations



def main():

    webscraper = Webscraper()
    result = webscraper.results()
    print(result)



class Webscraper:
    def __init__(self):
        self.search_input = self.get_input()
        self.urls1 = self.get_alternate_urls()
        self.urls2 = self.get_arlt_urls()
        self.urls3 = self.get_mindfactory_urls()
        self.all_cards = self.run()



    def get_input(self):
        raw_input = input("What do Graphics Card do you want: ").strip().split(" ")
        clean_input = [word.strip() for word in raw_input]
        return clean_input
    

    
    def run(self):
        with ProcessPoolExecutor() as executor:
            process1 = executor.submit(self.webscrape_alternate, self.alternate_thread)
            process2 = executor.submit(self.webscrape_arlt, self.arlt_thread)
            process3 = executor.submit(self.webscrape_mindfactory, self.mindfactory_thread)
            all_cards = process1.result() + process2.result() + process3.result()
        return all_cards

        

    def check_products(self, name_product) -> bool:
        """
        Check if the given user input is somewhere included in the graphics card name.
        If yes return true otherwise return false.
        """
        check = True
        for i in range(len(self.search_input)):
            if self.search_input[i] not in name_product.lower():
                check = False
        return check



    def get_alternate_urls(self):
        urls = []
        url = "https://www.alternate.de/Grafikkarten"
        count = 0
        scan_pages = 16
        while True:
            if count > scan_pages:
                break
            if count > 0:
                url = f"https://www.alternate.de/Grafikkarten?page={count}"
                urls.append(url)
            count += 1
        return urls



    def alternate_thread(self, alternate_url):
        cards = []
        html = requests.get(alternate_url).text
        soup = BeautifulSoup(html, "html.parser")
        product_names = soup.find_all("div", "product-name font-weight-bold")
        product_prices = soup.find_all("span", "price")
        product_links = soup.find_all("a", "card align-content-center productBox boxCounter text-font")
        for name, price, link in zip(product_names, product_prices, product_links):
            name = re.search(r'^<div class="product-name font-weight-bold"><span>(?:.*)</span>(.*)</div>$', str(name))
            price = re.search(r'^<span class="price">(.*)</span>$', str(price))
            #get links from the a tags store it in links
            link = link.get("href")
            #cleanup prices data -> remove € prefix, replace , with . and split the string at .
            #only take the first two elements of list into account join on .
            #convert price string into float into a float
            price = price.group(1).replace("€ ", "").replace(".", "_").replace(",", ".")
            price = float(price)
            #split the name variable into two variables
            name_product = name.group(1)
            #appending builder_name, name_product and price to products as a tuple
            if self.check_products(name_product) and (name_product, price, link) not in cards: 
                cards.append((name_product, price, link))
        return cards
                    

        
    def webscrape_alternate(self, alternate_thread):
        """
        Webscraper for graphics cards on alternate.de\n
        Runs through all pages and scrapes all graphics cards\n
        But only appending the graphics cards that meet the requiered input to the graphic_cards attribute
        """
        print("Start 1st process")
        with ThreadPoolExecutor() as executor:
            threads = executor.map(alternate_thread, self.urls1)
            cards = []
            for process in threads:
                for card in process:
                    cards.append(card)
        print("Finish 1st process")
        return cards
        
        

    def get_arlt_urls(self):
        urls = []
        scan_pages = 29
        count = 0
        url = "https://www.arlt.com/Hardware/PC-Komponenten/Grafikkarten/"
        while True:
            if count > scan_pages:
                break
            if count > 0:
                url = f"https://www.arlt.com/Hardware/PC-Komponenten/Grafikkarten/?pgNr={count}"
                urls.append(url)
            count += 1
        return urls



    def arlt_thread(self, arlt_url):
        cards = []
        html = requests.get(arlt_url).text
        soup = BeautifulSoup(html, "html.parser")
        products = soup.find_all("a", "productTitle")
        prices = soup.find_all("span", "lead price text-nowrap")
        for product, price in zip(products, prices):
            link = product.get("href")
            name_product = product.get_text().strip().lower()
            price = float(price.get_text()
                .strip()
                .lower()
                .replace("€", "")
                .replace(".", "_")
                .replace(",", ".")
            )
            if self.check_products(name_product) and (name_product, price, link) not in cards:
                cards.append((name_product, price, link))
        return cards



    def webscrape_arlt(self, arlt_thread):
        """
        Webscraper for graphics cards on mindfactory.de\n
        Runs through all pages and scrapes all graphics cards,\n
        but only appending the graphics cards that meet the requiered input to the graphic_cards attribute.
        """
        print("Start 2st process")
        with ThreadPoolExecutor() as executor:
            threads = executor.map(arlt_thread, self.urls2)
            cards = []
            for process in threads:
                for card in process:
                    cards.append(card)
        print("Finish 2st process")
        return cards



    def get_mindfactory_urls(self):
        urls = []
        count = 0
        scan_pages = 8
        url = "https://www.mindfactory.de/Hardware/Grafikkarten+(VGA).html"
        while True:
            if count > scan_pages:
                break
            if count > 0:
                url = f"https://www.mindfactory.de/Hardware/Grafikkarten+(VGA).html/page/{count+1}"
                urls.append(url)
            count += 1
        return urls



    def mindfactory_thread(self, mindfactory_url):
        cards = []
        html = requests.get(mindfactory_url).text
        soup = BeautifulSoup(html, "html.parser")
        product_names = soup.find_all("div", "pname")
        product_prices = soup.find_all("div", "pprice")
        links = soup.find_all("div", "pcontent")
        product_links = []
        for link in links:
            s = BeautifulSoup(str(link), "html.parser")
            link = s.find("a")['href']
            product_links.append(link)
        for name, price, link in zip(product_names, product_prices, product_links):
            name = re.search(r'^<div class="pname">(.+)</div>$', str(name))
            name_product = name.group(1)
            price = re.search(r'^<div class="pprice">.*<span class="text-currency">.*</span>(.+)</div>$', str(price))
            price = price.group(1)
            price = float(price.replace("-", "").replace("*", "").replace("</span>", "").replace(".", "_").replace(",", "."))
            if self.check_products(name_product) and (name_product, price, link) not in cards:
                cards.append((name_product, price, link))
        return cards



    def webscrape_mindfactory(self, mindfactory_thread):
        """
        Webscraper for graphics cards on mindfactory.de\n
        Runs through all pages and scrapes all graphics cards,\n
        But only appending the graphics cards that meet the requiered input to the graphic_cards attribute.
        """
        print("Start 3st process")
        with ThreadPoolExecutor() as executer:
            threads = executer.map(mindfactory_thread, self.urls3)
            cards = []
            for process in threads:
                for card in process:
                    cards.append(card)
        print("Finished 3st process")
        return cards



    def results(self, quantity=3) -> (list[tuple] | None):
        """
        Sort graphics cards that meet the requirement (user input),\n
        according to price from lowest price to highest price.\n
        Append as many elements as the specified quantity (default: 3) to the _results attribute\n
        Lastly remove every Item from the _results attribute, that costs less than 300€,\n
        because most of the time those items aren't graphics cards, but accesories.
        """
        cheapest_cards = []
        if self.all_cards:
            if len(self.all_cards) > quantity:
                for index, card in enumerate(sorted(self.all_cards, key=lambda card: card[1])):
                    if index > (quantity - 1):
                        break
                    cheapest_cards.append(card)
            else:
                for index, card in enumerate(sorted(self.all_cards, key=lambda card: card[1])):
                    if len(self.all_cards) == (index - 1):
                        break
                    cheapest_cards.append(card)
        else:
            print("No results found.")
            return None
        for index, card in enumerate(cheapest_cards):
            __, price, _ = card
            if price < 300:
                cheapest_cards.pop(index)
        return cheapest_cards






if __name__ == "__main__":
    main()