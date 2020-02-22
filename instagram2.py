from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import os
import cv2
import numpy as np
import urllib.request

class Instabot:

    def __init__(self, username, password):

        self.driver = webdriver.Firefox()
        self.username = username
        self.password = password

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        self.driver.get("https://www.instagram.com/") 
        time.sleep(2)

        login_button = self.driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']") 
        login_button.click()
        time.sleep(2)

        username_elem = self.driver.find_element_by_xpath("//input[@name='username']")
        username_elem.clear()
        username_elem.send_keys(self.username)

        password_elem = self.driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()
        password_elem.send_keys(self.password)
        password_elem.send_keys(Keys.RETURN)

        time.sleep(5)

    def likephoto(self, hashtag):
        
        self.driver.get("https://www.instagram.com/explore/tags/{}/".format(hashtag))
        time.sleep(5) 
        for i in range(5):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        hrefs = self.driver.find_elements_by_tag_name('a')
        pic_hrefs = [elem.get_attribute('href') for elem in hrefs]
        
        pic_hrefs = [href for href in pic_hrefs if hashtag in href]
        print(hashtag + 'photos: ', str(len(pic_hrefs)))
        
        for pic_href in pic_hrefs:
            self.driver.get(pic_href)
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            try:
                self.driver.find_element_by_link_text('Like').click()
                time.sleep(18)
            except:
                time.sleep(2)


    def get_following(self):
       

        self.driver.get("https://www.instagram.com/{}/".format(self.username))
        time.sleep(5)
        popup_button = self.driver.find_element_by_xpath("//a[@href='/{}/following/']".format(self.username)) 
        popup_button.click()
        time.sleep(5)

        lis = []
        follower_length = 0

        popup_follower = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        
        while(1):
            
            
            following_list = self.driver.find_elements_by_xpath("//a[@class='FPmhX notranslate _0imsa ']")
            
            for fl in following_list:
                if(fl.get_attribute('title') not in lis):
                    lis.append(fl.get_attribute('title'))

            
            popup_follower.send_keys(Keys.PAGE_DOWN)

            if(len(lis)==follower_length):
                break
            follower_length = len(lis)
            time.sleep(4)
            
            

        print(lis)
        
    def get_images(self, uid, path):
        
        self.driver.get("https://www.instagram.com/{}/".format(uid))
        time.sleep(5)
        SCROLL_PAUSE_TIME = 3


        last_height = self.driver.execute_script("return document.body.scrollHeight")
        images = []
        images2 = []
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    
            imag = self.driver.find_elements_by_xpath("//img[@class='FFVAD']")
            for item in imag:
                pt = item.get_attribute("src").split("?_nc")[0]
                if(pt not in images2):
                    images2.append(pt)
                    images.append(item.get_attribute("src"))
                    
        try:
            os.mkdir(path+'/{}'.format(uid))
        except:
            pass
        
        for idx, item in enumerate(images):
            
            url = item
            resp = urllib.request.urlopen(url)
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
           
            path2 = path+"/{}/{}.jpg".format(uid,idx)
            cv2.imwrite(path2, image)
            
            
       
            
        

    
username  = input('Enter The username: ')
password = input('Enter The password: ')
bot = Instabot(username, password)
bot.login()
# time.sleep()
# bot.likephoto('japan')
# bot.get_following()
bot.get_images('vewn_', './img')
# bot.closeBrowser()


