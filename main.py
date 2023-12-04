import threading
import time

import web_scraper
import whatsapp_operations





def main():

    start = time.time()

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
    results = scraper.results(quantity=7)

    #for each graphics card in results send a whatsapp message with the graphics card details 

    whatsapp = whatsapp_operations.WhatsAppAPI(instance_id="<instance_id_from_greenApi>", api_key="<api_key_from_greenApi>")    
    for card in results:
        
        name, price, link = card
        message = f"New lowest Price for {name}\n\nPrice: {price}€\n\nLink: {link}"
        whatsapp.send_message(message, "<chat_id")

    
    print(time.time() - start)





if __name__ == "__main__":
    main()
