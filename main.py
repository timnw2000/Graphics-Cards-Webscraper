import os
import threading
import time

from cryptography.fernet import Fernet

import web_scraper
import whatsapp_operations





def main():

    #create Webscraper Object
    scraper = web_scraper.Webscraper()

    #get input (which graphics card)
    scraper.get_input()

    #start first thread for searching first website
    t1 = threading.Thread(target=scraper.webscrape_mindfactory, daemon=True)
    t1.start()

    #start second thread for searching second website
    t2 = threading.Thread(target=scraper.webscrape_alternate, daemon=True)
    t2.start()
    
    #start searching in main thread for third website
    scraper.webscrape_arlt()

    #waiting for the threads to execute
    t1.join()
    t2.join()

    #storing the results of the search with the given input in the results variable
    results = scraper.results(quantity=3)
    
    
    
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
    for card in results:
        
        name, price, link = card
        message = f"New lowest Price for {name}\n\nPrice: {price}€\n\nLink: {link}"


        whatsapp.send_message(message, f"{access[3].decode()}")

    



if __name__ == "__main__":
    main()
