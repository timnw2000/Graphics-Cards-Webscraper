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

    whatsapp = whatsapp_operations.WhatsAppAPI(instance_id="7103879645", api_key="f6bd92a04c634ba18277df578a753341c4461bad7b3b435cae")    
    for card in results:
        
        name, price, link = card
        message = f"New lowest Price for {name}\n\nPrice: {price}€\n\nLink: {link}"
        whatsapp.send_message(message, "4915733883576")

    
    print(time.time() - start)





if __name__ == "__main__":
    main()