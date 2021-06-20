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
from datetime import datetime

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

    def SaveTodaysDataFile(self):
        today = datetime.today()
        self.extract_dt = today.strftime("%m/%d/%Y, %H:%M:%S")
        self.extract_day_id = today.strftime('%Y%m%d')
        thisdir = os.getcwd()
        fileToSave = thisdir + '\\historical_data\\' + self.extract_day_id + '\\{}_extract_{}.json'.format(self.zipcode,self.extract_day_id)
        daydirectory = thisdir + '\\historical_data\\' + self.extract_day_id + '\\'
        if not os.path.exists(daydirectory):
            os.makedirs(daydirectory)

        with open(fileToSave,"w") as outfile:
            json.dump(self.__dict__,outfile,indent=4,sort_keys=True)



    def FileSavedForToday(self):
        today = datetime.today()
        self.extract_dt = today.strftime("%m/%d/%Y, %H:%M:%S")
        self.extract_day_id = today.strftime('%Y%m%d')
        thisdir = os.getcwd()
        fileToSave = thisdir + '\\historical_data\\' + self.extract_day_id + '\\{}_extract_{}.json'.format(self.zipcode,self.extract_day_id)

        print(fileToSave)

        if os.path.exists(fileToSave):
            return True
        else:
            return False




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

    if objMyPropertySearchInfo.FileSavedForToday():
        return

    thisdir = os.getcwd()
    chromedirver = thisdir + '\\chromedriver\\chromedriver.exe'

    driver = webdriver.Chrome(executable_path=chromedirver)

    driver.get(objMyPropertySearchInfo.analytics_uri)
    #assert "python" in driver.title
    timeout = 40
    #wait otherwise Realtor will shut the browser down
    WebDriverWait(driver,(timeout*8))
    elem = None
    listing_count = ""
    try:
        elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/section[1]/section[2]/div[2]/section[2]/div/div[2]/div[1]/span/span")
        listing_count = elem.text
    except:
        try:
            elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/section[1]/section[2]/div[2]/section[1]/div/div[2]/div[1]/span/span/")
            listing_count = elem.text
        except:
            fido="dido"
    try:
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

        kresult = re.search('\.(.*)k', elem.text)

        k_zeropadder={
            1: "00",
            2: "0"
        }

        if kresult:
            zeroreplacer = k_zeropadder.get(int(len(kresult.group(1))))

        mprice = locale.format("%d", int(elem.text.replace("$","").replace(".","").replace("M",zeroreplacer).replace("k",zeroreplacer)), grouping=True)
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
    except:
        objMyPropertySearchInfo.extract_error = "true"

    WebDriverWait(driver,(timeout*10))

    driver.get(objMyPropertySearchInfo.price_reduced_status)

    l_reduced_prices_xpath = []
    l_reduced_prices_xpath.append("/html/body/div[1]/div[7]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]")
    l_reduced_prices_xpath.append("/html/body/div[1]/div[8]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]")
    matched = False
    elem = None
    xpath_to_use=None
    for x_path in l_reduced_prices_xpath:
        try:
            elem = driver.find_element_by_xpath(x_path)
            matched = True
            xpath_to_use = x_path
            break
        except:
            continue

    if(matched):
        elem = driver.find_element_by_xpath(xpath_to_use)
        rresult = re.search('Showing (.*) Home', elem.text)

        reduced_today = 0

        if rresult:
            reduced_today = int(rresult.group(1))
            objMyPropertySearchInfo.price_reduced_today = reduced_today


    WebDriverWait(driver,(timeout*10))

    driver.close()

    objMyPropertySearchInfo.SaveTodaysDataFile()





def main():
    print('in main')
    myPropertySearchObjectsList = LoadPropertySearchInfo()

    for searchObject in myPropertySearchObjectsList:
        PerformPropertySearchSaveResults(searchObject)
        #searchObject.PrintInternalDictionary()

main()




