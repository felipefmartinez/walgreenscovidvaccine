#! /usr/bin/python
from selenium import webdriver
import time
import ctypes  # An included library with Python install.
import os, fnmatch, shutil  
import smtplib, ssl  
import telegram_send

def send_email(addr, pswrd, mesg):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(addr, pswrd)
    subject = "Walgreens Vaccine Available!"
    body = "This zip code tested green just now " + mesg + ":\n"
    msg = 'Subject: {}\n\n{}'.format(subject, body)
    server.sendmail(addr, "YOUREMAIL@gmail.com", msg)
    server.quit()
def storescores(writethis):
    t = time.localtime()
    timestamp = time.strftime('%b-%d %H:%M:%S', t)
    hs = open("zipcodes.txt","a")
    hs.write(writethis + " " + timestamp)
    #hs.write(now)
    hs.write("\n")
    hs.close()

zipdict = {}
zip_codes =['20106','20110']
for zips in zip_codes:
    zipdict[zips] = 'RED'
my_options = webdriver.ChromeOptions()
my_options.add_argument("headless")
my_options.add_argument("no-referrers")
driver = webdriver.Chrome("C:\\Users\\username\\Documents\\chromedriver\\chromedriver.exe", options=my_options) 
driver.get("https://www.walgreens.com/findcare/vaccination/covid-19?ban=covid_vaccine_landing_schedule")
#driver.get("https://www.walgreens.com/findcare/vaccination/covid-19/location-screening")
start_button = driver.find_element_by_class_name('btn.btn__blue')
start_button.click()
found = False
while found == False:
    for zips in zip_codes:
        driver.implicitly_wait(5)
        location_text = driver.find_element_by_id('inputLocation')
        location_text.clear()
        location_text.send_keys(zips)

        location_button = driver.find_element_by_class_name('btn')
        location_button.click()
        
        driver.implicitly_wait(5)
        try:
            alert = driver.find_element_by_class_name('alert.alert__red')
            if zipdict[zips] == 'GREEN':
                    zipdict[zips] = 'RED'
        except:
            try:
                alert = driver.find_element_by_class_name('alert.alert__green')
                if zipdict[zips] == 'RED':
                    print('FOUND' + zips)
                    storescores(zips)
                    telegram_send.send(messages=[zips])
                    zipdict[zips] = 'GREEN'
                else:
                    print('Was already green')
            except:
                print('ERROR ' + zips)
    time.sleep(1)
