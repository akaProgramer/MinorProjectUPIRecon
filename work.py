
import requests
import concurrent.futures
import main
from time import sleep
from sys import exit
from random import uniform as rand
from datetime import datetime


API_URL = 'https://upibankvalidator.com/api/upiValidation?upi='


#  opting to load lists from a file instead of hardcoding them
#  as this would be more flexible, allow for easier updates,
#  and allow others to make use of the lists provided
with open("data/general_suffixes.txt", "r") as suffix_file:
    upi_suffix_dict = suffix_file.read().splitlines() #  read all suffixes into a list

with open("data/mobile_suffixes.txt", "r") as mobile_suffix_file:
    mobile_suffix_dict = mobile_suffix_file.read().splitlines()

with open("data/fastag_suffixes.txt", "r") as fastag_suffix_file:
    fastag_suffix_dict = fastag_suffix_file.read().splitlines()

with open("data/gpay_suffixes.txt", "r") as gpay_suffix_file:
    gpay_suffix_dict = gpay_suffix_file.read().splitlines()



class Scraper:
    # finished = pyqtSignal()
    # progress = pyqtSignal(int)
    found = 0
    count = 0
    def searchvpa(self, searchtext, vpa_dict, threadcount):
        if(threadcount == 0):
            for suffix in vpa_dict:
                try:
                    self.address_discovery(searchtext + '@' + suffix, API_URL)
                except KeyboardInterrupt:
                    exit(0)
        else:
            threadcount = 10 if threadcount > 10 else threadcount
            with concurrent.futures.ThreadPoolExecutor(max_workers=threadcount) as executor:
                try:
                    for suffix in vpa_dict:
                        executor.submit(self.address_discovery, searchtext + '@' + suffix, API_URL)
                        sleep(rand(.1, .2))
                        
                except KeyboardInterrupt:
                    #  quit ungracefully on keyboard interrupt:
                    #  considering the bandwidth consumed for requests,
                    #  there is no reason to wait for the threads to finish
                    #  sorry for the inconvenience
                    executor._threads.clear()
                    concurrent.futures.thread._threads_queues.clear()
        if self.found == 0:
            print("not found")
        
    def address_discovery(self, vpa, api_url):
        r = requests.post(api_url+vpa)

        print(r.status_code)
        if r.status_code == 200 and r.json()['isUpiRegistered'] is True:
            print(r.json()['name'])
            print(vpa)
            self.found += 1
        if r.status_code == 400:
            print("Bad Request")
        if r.status_code == 429:
            print("Too Many Requests")
        self.count += 1
    # def run(self):
    #     self.searchvpa("harshp2035", upi_suffix_dict, 10)

if __name__=="__main__":
    s= Scraper()
    s.run()