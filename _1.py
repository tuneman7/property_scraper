#!/usr/bin/python

import sys, getopt,os,smtplib,json,selenium,re, locale
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class PropertySearchInfo:

    def __init__(self,**kwargs):
        allowed_keys = {'zipcode', 'search_uri', 'description'}
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)

    def __init__(self,jsonString):
        self.__dict__ = json.loads(jsonString)

    def PrintInternalDictionary(self):
        for k,v in self.__dict__.items():
            print("{} is \"{}\"".format(k,v))


class PropertyListing:

    def __init__(self):
        fido="dido"



def LoadPropertySearchInfo():
    loutput = []
    thisdir = os.getcwd()
    searchParameterFile = thisdir + '\\driver_data\\_redfin.json'

    with open(searchParameterFile) as f:
        mySearchInfo = json.load(f)

        for search in mySearchInfo["property_searches"]:
            for realtorsearch in search["realtor.com"]:

                myPropertySearchInfo = PropertySearchInfo(json.dumps(realtorsearch))
                #myPropertySearchInfo.PrintInternalDictionary()
                #print(myPropertySearchInfo)
                loutput.append(myPropertySearchInfo)

    return loutput


def PerformPropertySearchSaveResults(objMyPropertySearchInfo):
    objMyPropertySearchInfo.PrintInternalDictionary()
    thisdir = os.getcwd()
    chromedirver = thisdir + '\\chromedriver\\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=chromedirver)
    driver.get(objMyPropertySearchInfo.analytics_uri)
    #assert "python" in driver.title
    timeout = 5
    WebDriverWait(driver,(timeout*2))
    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/section[1]/section[2]/div[2]/section[2]/div/div[2]/div[1]/span/span")
    #result = re.search('There are (.*) homes', elem.text)
    objMyPropertySearchInfo.active_listings = elem.text

    if elem.get_attribute("innerHTML").find("arrow-up") !=-1:
        objMyPropertySearchInfo.active_listings_up_down = "up"
    else:
        objMyPropertySearchInfo.active_listings_up_down = "down"


    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/section[1]/section[2]/div[2]/section[2]/div/div[1]/div[1]/span/span")
    locale.setlocale(locale.LC_ALL, 'en_US')
    textprice = elem.text.strip()
    zeroreplacer = ""

    mresult = re.search('\.(.*)M', elem.text)

    mil_zeropadder={
        1:"00000",
        2:"0000",
        3:"000"
    }

    if mresult:
        zeroreplacer = mil_zeropadder.get(int(len(mresult.group(1))))

    kresult = re.search('\$(.*)K', elem.text)

    if kresult:
        zeroreplacer = "000"


    mprice = locale.format("%d", int(elem.text.replace("$","").replace(".","").replace("M",zeroreplacer).replace("K",zeroreplacer)), grouping=True)
    objMyPropertySearchInfo.median_list_price = mprice
    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/section[1]/section[2]/div[2]/section[2]/div/div[1]/div[1]/span/span")

    if elem.get_attribute("innerHTML").find("arrow-up") !=-1:
        objMyPropertySearchInfo.median_list_price_up_down = "up"
    else:
        objMyPropertySearchInfo.median_list_price_up_down = "down"


    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/section[1]/section[2]/div[2]/section[2]/div/div[1]/div[3]/span/span")
    objMyPropertySearchInfo.median_price_per_sqft = elem.text.replace("$","")

    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/section[1]/section[2]/div[2]/section[2]/div/div[1]/div[3]/span/span")

    if elem.get_attribute("innerHTML").find("arrow-up") !=-1:
        objMyPropertySearchInfo.median_price_per_sqft_up_down = "up"
    else:
        objMyPropertySearchInfo.median_price_per_sqft_up_down = "down"

    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/section[1]/section[2]/div[2]/section[2]/div/div[1]/div[2]/span/span")
    objMyPropertySearchInfo.average_days_on_market = elem.text

    if elem.get_attribute("innerHTML").find("arrow-up") !=-1:
        objMyPropertySearchInfo.average_days_on_market_up_down = "up"
    else:
        objMyPropertySearchInfo.average_days_on_market_up_down = "down"

    WebDriverWait(driver,(timeout*2))

    driver.get(objMyPropertySearchInfo.price_reduced_status)

    elem = driver.find_element_by_xpath("/html/body/div[1]/div[6]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]")

    rresult = re.search('Showing (.*) Homes', elem.text)

    reduced_today = 0

    if rresult:
        reduced_today = int(rresult.group(1))

    objMyPropertySearchInfo.price_reduced_today = reduced_today


    WebDriverWait(driver,(timeout*2))

    #assert "No results found." not in driver.page_source
    driver.close()


def main():
    print('in main')
    myPropertySearchObjectsList = LoadPropertySearchInfo()

    for searchObject in myPropertySearchObjectsList:
        PerformPropertySearchSaveResults(searchObject)
        #searchObject.PrintInternalDictionary()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/


