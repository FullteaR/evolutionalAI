import sys
import json
import os
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions
from selenium import webdriver
from bs4 import BeautifulSoup
import time

options=Options()
options.add_argument("-headless")
driver = webdriver.Firefox(firefox_options=options)

def scraping(command,url="http://0.0.0.0:8080/hatetris.html"):
    command+="A"*200

    # Selenium settings
    # get a HTML response
    driver.get(url+"?command="+command)
    driver.find_element_by_class_name("replayButton").click()
    replay=None
    while replay==None:
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        replay=soup.find(class_="hatetris__replay-out").string

        time.sleep(0.1)


    score=soup.find(class_="hatetris__score")
    return int(score.string)





    #fp=open("/Users/rikutamba/Desktop/hatetris/src/html/bundle.js","w")
    #fp.writelines(body)


if __name__ == '__main__':
    # arguments
    url="http://0.0.0.0:8080/hatetris.html"

    print(scraping("0"*1000+"A"*200))
