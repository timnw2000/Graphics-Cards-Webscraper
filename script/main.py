import os
import threading
import time
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
from cryptography.fernet import Fernet

import web_scraper
import whatsapp_operations


splitted = input("Which Graphics Card do you want to find: ").lower().split(" ")
search_input = [word.strip() for word in splitted]


def main():
    start = time.time()
    urls1 = web_scraper.get_alternate_urls()
    urls2 = web_scraper.get_arlt_urls()
    urls3 = web_scraper.get_mindfactory_urls()
    with ProcessPoolExecutor() as executor:
        process1 = executor.submit(web_scraper.webscrape_alternate, web_scraper.alternate_thread, urls1)
        process2 = executor.submit(web_scraper.webscrape_arlt, web_scraper.arlt_thread, urls2)
        process3 = executor.submit(web_scraper.webscrape_mindfactory, web_scraper.mindfactory_thread, urls3)
        
        all_cards = process1.result() + process2.result() + process3.result()
        

    found_cards = web_scraper.results(all_cards)


    if os.path.exists("./token.txt"):
        access = []
        with open("token.txt", "rb") as token:
            for line in token:
                access.append(line)
        
        fernet = Fernet(access[0].decode())
        whatsapp = whatsapp_operations.WhatsAppAPI(instance_id=f"{fernet.decrypt(access[1]).decode()}", api_key=f"{fernet.decrypt(access[2]).decode()}")
    else:
        access = []
        key = Fernet.generate_key()
        fernet = Fernet(key)
        access.append(key + b"\n")

        instance_id = input("Instance_id from GreenAPI: ").strip()
        api_key = input("Api_Key from GreenAPI: ").strip()
        chat_id = input("Chat_id from GreenAPI (usually your phone number +49 111222333444 -> chat_id 49111222333444): ").strip()
        access.append(fernet.encrypt(instance_id.strip().encode()) + b"\n")
        access.append(fernet.encrypt(api_key.strip().encode()) + b"\n")
        access.append(chat_id.encode())

        with open("token.txt", "wb") as token:
            for line in access:
                token.write(line)
        whatsapp = whatsapp_operations.WhatsAppAPI(instance_id=instance_id, api_key=api_key)
    

    #for each graphics card in results send a whatsapp message with the graphics card details 
    for card in found_cards:
        
        name, price, link = card
        message = f"New lowest Price for {name}\n\nPrice: {price}€\n\nLink: {link}"


        whatsapp.send_message(message, f"{access[3].decode()}")


    print(time.time() - start)

if __name__ == "__main__":
    main()
