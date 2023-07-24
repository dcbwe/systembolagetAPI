import requests
import json
import sqlite3
from sqlite3 import Error
import time
import random

class SystembolagetAPI:

    def __init__(self):
        self.session = requests.session()
        self.start()



    #Last updated 2023/03/28
    def getUserAgent(self):

        userAgents = {
            "1": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:111.0) Gecko/20100101 Firefox/111.0",
            "2": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.3; rv:111.0) Gecko/20100101 Firefox/111.0",
            "3": "Mozilla/5.0 (X11; Linux x86_64; rv:111.0) Gecko/20100101 Firefox/111.0",
            "4": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:111.0) Gecko/20100101 Firefox/111.0",
            "5": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:111.0) Gecko/20100101 Firefox/111.0",
            "6": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:111.0) Gecko/20100101 Firefox/111.0",
            "7": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "8": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.3; rv:102.0) Gecko/20100101 Firefox/102.0",
            "9": "Mozilla/5.0 (X11; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0",
            "10": "Mozilla/5.0 (Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "11": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0",
            "12": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "13": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "14": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "15": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "16": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "17": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "18": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "19": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"
        }

        return userAgents[f"{random.randint(1, 19)}"]
    

    
    def getHeader(self):

        userAgent = self.getUserAgent()

        headers = {
            "User-Agent": f"{userAgent}",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Access-Control-Allow-Origin": "*",
            "Connection": "keep-alive",
            "Content-Type":"application/json",    
            "DNT": "1",
            "Ocp-Apim-Subscription-Key":"cfc702aed3094c86b92d6d4ff7a54c84",
            "Origin":"https://www.systembolaget.se",
            "Referer":"https://www.systembolaget.se/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
            "x-nextjs-data":"1"    
            }
        
        return headers




    def systembolagetAPI(self, page, size):

        #Keep count during runtime
        counter = self.countProducts()

        ###
        isTrue = True

        #Create DB and connection
        with self.createConnection('systemet.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS products
                       (id INTEGER PRIMARY KEY, product_data TEXT)''')

        #Url for session
        url = "https://api-systembolaget.azure-api.net/sb-api-ecommerce/v1/productsearch/search"

        
        #Is True for as long as response 200 | Will run for a while...
        while isTrue:
      

            page += 1

            params = {
            "page": page,
            "size": size,
            "sortBy": "Score",
            "sortDirection": "Ascending",
            "status": "Active"
            }


            #Necessary precaution
            HEADERS = self.getHeader()
            
            
            response = self.requestsCall(url, params, HEADERS)

                
            if response.status_code == requests.codes.ok:
                products = json.loads(response.text)['products']

                for product in products:
                    next(counter)
                    product_data = json.dumps(product, ensure_ascii=False)
                    cursor.execute('INSERT OR IGNORE INTO products (product_data) VALUES (?)', (product_data,))

                conn.commit()

            else:
                isTrue = False

        conn.close()
            


    def requestsCall(self, url, params, HEADERS):

        #Returns 0 when tryblock fails
        response = requests.Response()
        response.status_code = 0


        #Timeout set to 30sec, feel free to adjust if needed
        try:
            response = self.session.get(url, params=params, headers=HEADERS, timeout=30)

        except requests.Timeout:
            print("Timeout")

        except requests.ConnectionError:
            print("Something went wrong")

        finally:   
            return response
        

        
    def countProducts(self):
        plusOne = 0
        while True:
            yield print(plusOne)
            plusOne += 1



    def createConnection(self, database):
        connection = None
        try:
            connection = sqlite3.connect(database)
        except Error as e:
            raise(e)
        return connection



    def start(self):
        
        #For the curious mind
        startTime = time.time()

        #Startpage
        page = 0

        #Set size of products/page 
        size = 30

        
        self.systembolagetAPI(page, size)

        timeCount = time.time() - startTime
        print(f"Finished in {timeCount} seconds")


if __name__ == "__main__":
    SystembolagetAPI()
