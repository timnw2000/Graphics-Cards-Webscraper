import requests
from bs4 import BeautifulSoup
import re





class Webscraper:
    def __init__(self):
        self.search_modell = None
        self.graphic_cards = []
        self._results = []



    
    def get_input(self) -> list[str]:
        """
        Ask for user input\n
        Split user input into a list\n
        Each element represents one word in the users input
        """
        user_input = input("Which Graphics Card do you want: ")
        #strip leading and ending whitespaces and turn the input into a list with words as elements
        user_input = user_input.lower().strip().split()
        #cleanup elements in the list
        for element in user_input:
            element = element.strip()
        #return list
        self.search_modell = user_input
        return user_input
    


        
    def webscrape_alternate(self):

        """
        Webscraper for graphics cards on alternate.de\n
        Runs through all pages and scrapes all graphics cards\n
        But only appending the graphics cards that meet the requiered input to the graphic_cards attribute
        """

        url = "https://www.alternate.de/Grafikkarten"
        search_input = self.search_modell 
        products = []
        count = 0
        scan_pages = 16
        repeat_counter = 0

        while True:
            if count > scan_pages:
                break
            if count > 0:
                url = f"https://www.alternate.de/Grafikkarten?page={count}"

            html = requests.get(url).text

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
                if ((name_product, price, link) not in self.graphic_cards) and self.check_products(name_product, search_input): 
                    self.graphic_cards.append((name_product, price, link))

            count += 1
        



    def webscrape_mindfactory(self):

        """
        Webscraper for graphics cards on mindfactory.de\n
        Runs through all pages and scrapes all graphics cards,\n
        But only appending the graphics cards that meet the requiered input to the graphic_cards attribute.
        """

        count = 0
        
        search_input = self.search_modell
        scan_pages = 8
        url = "https://www.mindfactory.de/Hardware/Grafikkarten+(VGA).html"

        while True:
            if count > scan_pages:
                break
            if count > 0:
                    url = f"https://www.mindfactory.de/Hardware/Grafikkarten+(VGA).html/page/{count+1}"

            html = requests.get(url).text

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


                if ((name_product, price, link) not in self.graphic_cards) and self.check_products(name_product, search_input):
                    self.graphic_cards.append((name_product, price, link))

            count += 1
        



    def webscrape_arlt(self):

        """
        Webscraper for graphics cards on mindfactory.de\n
        Runs through all pages and scrapes all graphics cards,\n
        but only appending the graphics cards that meet the requiered input to the graphic_cards attribute.
        """

        scan_pages = 29
        search_input = self.search_modell
        count = 0
        url = "https://www.arlt.com/Hardware/PC-Komponenten/Grafikkarten/"
        while True:
            if count > scan_pages:
                break
            if count > 0:
                url = f"https://www.arlt.com/Hardware/PC-Komponenten/Grafikkarten/?pgNr={count}"

            html = requests.get(url).text
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
                if ((name_product, price, link) not in self.graphic_cards) and self.check_products(name_product, search_input):
                    self.graphic_cards.append((name_product, price, link))
                
            count += 1




    def check_products(self, name_product, search_input) -> bool:
        """
        Check if the given user input is somewhere included in the graphics card name.
        If yes return true otherwise return false.
        """

        check = True
        for i in range(len(search_input)):
            if search_input[i] not in name_product.lower():
                check = False
                
        return check

    


    def results(self, quantity=3) -> (list[tuple] | None):
        
        """
        Sort graphics cards that meet the requirement (user input),\n
        according to price from lowest price to highest price.\n
        Append as many elements as the specified quantity (default: 3) to the _results attribute\n
        Lastly remove every Item from the _results attribute, that costs less than 300€,\n
        because most of the time those items aren't graphics cards, but accesories.
        """

        if self.graphic_cards:
            
            if len(self.graphic_cards) > quantity:
                for index, card in enumerate(sorted(self.graphic_cards, key=lambda card: card[1])):
                    if index > (quantity - 1):
                        break
                    self._results.append(card)

            else:
                for index, card in enumerate(sorted(self.graphic_cards, key=lambda card: card[1])):
                    if len(self.graphic_cards) == (index - 1):
                        break
                    self._results.append(card)
        else:
            print("No results found.")
            return None

        for index, card in enumerate(self._results):
            name, price, link = card
            if price < 300:
                self._results.pop(index)

        return self._results