#30xbot
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import random
import smtplib
import time
import bb_info
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import re
import pickle
from telegram.ext import Updater
import logging
import telebot
import mysql.connector
from datetime import date

followers = []
random_int = random.randint(0, 4)

def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(bb_info.EMAIL_ADDRESS, bb_info.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(bb_info.EMAIL_ADDRESS, 'bern----wnsa@gmail.com', message)
        server.quit()
        print('SUCCESS: email sent')
    except:
        print('ERROR: email failed to send')

class InstagramBot():

	def __init__(self, email, password):
		self.browserProfile = webdriver.ChromeOptions()
		chrome_options = Options()
		self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

		#self.browserProfile.add_argument("--user-data-dir=C:/Users/bbrow-------le/Chrome/User Data")
		self.browserProfile.add_argument("user-data-dir=C:/Users/b------ocal/Google/Chrome/User Data") #Path to your chrome profile
		self.browser = webdriver.Chrome('chromedriver.exe', options=self.browserProfile)
		#self.browser = webdriver.Firefox()
		self.email = email
		self.password = password
		self.browser.set_window_size(1000, 900)

	def clean_and_like(self,new_list,mylist):
		counter = 0
		#This removes the ones you've already liked
		for each in new_list:
			if each in mylist:
				new_list.remove(each)
				print('Already liked',each)

		bot.load_cookies()
		for each in new_list:
			each = each.replace("'",'')
			counter += 1
			try:
				bot.like_photo(each)
				t = time.localtime()
				today_date = date.today()
				today_date = str(today_date)
				today_time = time.strftime("%H:%M:%S", t)
				fullstring = today_date+' - '+today_time
				bot.insert_database(each,fullstring)
			except Exception as e:
				print(e)
			print('status: ',counter,'/',len(new_list))

		print('You liked',len(mylist),'pictures')

	def grand_likes(self, grand_list, mylist):
		print('Asking for Grand list')
		self.browser.get(grand_list)
		time.sleep(5)
		xo = self.browser.find_element_by_xpath('//div[@class="composer_rich_textarea"]')
		time.sleep(1)
		xo.click()
		time.sleep(1)
		xo.send_keys('/list')
		xo.send_keys(Keys.ENTER)
		time.sleep(10)
		self.browser.get('https://web.telegram.org/#/im?p=@travelgroupengV2bot')#This is the link to the list
		time.sleep(5)

		elems = self.browser.find_elements_by_xpath("//a[@href]")
		time.sleep(2)
		print('Len of all elems:',len(elems))
		new_list = []
		mylist = list(dict.fromkeys(mylist))
		print("Before for loop")
		for each in elems:
			try:
				if('http' in each.text):
					new_list.append(each.text)
			except:
				print("error")
		print("After for loop")
		new_list = new_list[-52:-2]
		print('This is the list:')
		print(new_list)
		return new_list

	def post_grand_likes(self, grand_list, newest_post):
		self.browser.get(grand_list)
		time.sleep(5)
		x = self.browser.find_element_by_xpath('//div[@class="composer_rich_textarea"]')
		x.click()
		x.send_keys('Dx50 - '+newest_post)
		x.send_keys(Keys.ENTER)

	def flash_engagement(self, flash_list, mylist):
		print('Asking for Flash list')
		self.browser.get(flash_list)
		time.sleep(5)
		xo = self.browser.find_element_by_xpath('//div[@class="composer_rich_textarea"]')
		time.sleep(1)
		xo.click()
		time.sleep(1)
		xo.send_keys('/list')
		xo.send_keys(Keys.ENTER)
		time.sleep(10)
		self.browser.get('https://web.telegram.org/#/im?p=@GetListsBot')
		time.sleep(5)

		elems = self.browser.find_elements_by_xpath("//a[@href]")
		print('Len of all elems:',len(elems))
		new_list = []
		mylist = list(dict.fromkeys(mylist))
		for each in elems:
			if('http' in each.text):
				new_list.append(each.text)
		new_list = new_list[-30:]
		print('This is the list:')
		print(new_list)
		return new_list

	def post_flash_engagement(self, flash_list, newest_post):
		self.browser.get(flash_list)
		time.sleep(5)
		x = self.browser.find_element_by_xpath('//div[@class="composer_rich_textarea"]')
		x.click()
		x.send_keys('Dx30 - '+newest_post)
		x.send_keys(Keys.ENTER)

	def get_database(self):
		mydb = mysql.connector.connect(
			host="localhost",
			user="username",
			passwd="password"
		)

		mycursor = mydb.cursor()

		mycursor.execute('use instagram_rhinowallet;')
		mycursor.execute('select photo from liked_photos;')

		sql_list = []
		for x in mycursor:
			x = str(x)
			x = x.replace('(','')
			x = x.replace(')','')
			x = x.replace("'",'')
			x = x.replace(',','')
			sql_list.append(x)

		return sql_list

	def insert_database(self,url,date):
		mydb = mysql.connector.connect(
		  host="localhost",
		  user="username",
		  passwd="password"
		)
		mycursor = mydb.cursor()
		sql = 'INSERT INTO liked_photos (photo,date) VALUES ("{}","{}");'.format(url, date)
		print("")
		print(sql)
		print("")
		mycursor.execute('use instagram_rhinowallet;')
		mycursor.execute(sql)
		for x in mycursor:
		  print(x)
		mydb.commit()

	def save_cookies(self):
		self.browser.get('https://www.instagram.com/rhinowallet/')
		time.sleep(6)
		pickle.dump(self.browser.get_cookies() , open("instagramlogincookies.pkl","wb"))
		print('cookies saved')
	def load_cookies(self):
		self.browser.get('https://www.instagram.com/rhinowallet/')
		cookies = pickle.load(open("instagramlogincookies.pkl", "rb"))
		for cookie in cookies:
			self.browser.add_cookie(cookie)
		self.browser.get('https://www.instagram.com/rhinowallet/')
	def signIn(self):
		self.browser.get('https://www.instagram.com/accounts/login/')
		time.sleep(5)
		emailInput = self.browser.find_elements_by_css_selector('form input')[0]
		passwordInput = self.browser.find_elements_by_css_selector('form input')[1]

		emailInput.send_keys(self.email)
		passwordInput.send_keys(self.password)
		passwordInput.send_keys(Keys.ENTER)
		time.sleep(2)

	def like_photo(self, newurl):
		self.browser.get(newurl)
		#self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(random.randint(1, 2))
		like_button = self.browser.find_element_by_xpath('//span[@aria-label="Like"]')
		self.browser.execute_script("arguments[0].click();", like_button)
		time.sleep(1)		
		like_button_2 = self.browser.find_element_by_xpath('//span[@class="glyphsSpriteHeart__filled__24__red_5 u-__7"]')
		print("Successfully liked.",like_button_2.get_attribute("aria-label"))

	def standard_telegram(self):
		self.browser.get('https://www.instagram.com/rhinowallet/')
		bot.load_cookies()
		self.browser.get('https://www.instagram.com/rhinowallet/')
		file = open('Desktop/telegram1.txt', 'r')
		count = 0
		for line in file:
			line = line[3:]
			line = line.replace(' ','')
			print(count,'- Now liking:',line)
			bot.like_photo(line)
			count += 1

	def get_recent(self):
		self.browser.get('https://www.instagram.com/rhinowallet/')
		bot.load_cookies()
		time.sleep(2)
		allposts = self.browser.find_elements_by_xpath('//div[@class="v1Nh3 kIKUG  _bz0w"]')
		allposts[0].click()
		newest_post = self.browser.current_url
		return newest_post

	def main(self):
		ultra_list = 'https://web.telegram.org/#/im?p=s1350238809_4011964756744671267'
		flash_list = 'https://web.telegram.org/#/im?p=@FlashInstagramLike'
		grand_list = 'https://web.telegram.org/#/im?p=s1294267426_17543255754256562168'

		self.browser.get(ultra_list)#This doesnt matter. It just opens the browser
		input('Enter key to continue')
		print('Thank you')
		while True:
			try:
				mylist = bot.get_database()
				newest_post = bot.get_recent()
				print('This is newest post:',newest_post)
				t = time.localtime()
				current_time = time.strftime("%H", t)
				current_time = int(current_time)
				if((22 <= current_time) or (6 >= current_time)):
					print(current_time,'Its late... so extra 45min sleep')
					#Extra 30min sleep if its past 10pm and before 7am
					time.sleep(1800)
				time.sleep(5)

				# Liking group number 2
				# --------------------------------------------------------------
				new_list = bot.grand_likes(grand_list,mylist)
				#---------------------------------------------------------------
				#--------------------------------------------------------------
				bot.clean_and_like(new_list,mylist)
				# -------------------------------------------------------------
				#--------------------------------------------------------------
				bot.post_grand_likes(grand_list, newest_post)
				#--------------------------------------------------------------
				mylist = bot.get_database()
				# --------------------------------------------------------------
				#Liking group number 1
				# --------------------------------------------------------------
				new_list = bot.flash_engagement(flash_list,mylist)
				#---------------------------------------------------------------
				#--------------------------------------------------------------
				bot.clean_and_like(new_list,mylist)
				# -------------------------------------------------------------
				#--------------------------------------------------------------
				bot.post_flash_engagement(flash_list, newest_post)
				#--------------------------------------------------------------
				mylist = bot.get_database()
				# --------------------------------------------------------------

				minute = 0
				r1 = random.randint(60, 90)
				while(minute < r1):
					print((r1-minute),' minutes left')
					minute += 1
					time.sleep(60)
			except Exception as e:
				print('Major Error: Will retry in 1min:',e)
				time.sleep(60)
				self.browser.set_window_size(1000, 900)
				time.sleep(5)
	
bot = InstagramBot('insta_username', 'insta_password')
print('Would you like to run automatic(a) or standard(s)? or open test? (t)')
i = input()
if(i == 'a'):
	bot.main()
elif(i == 's'):
	bot.standard_telegram()
elif(i == 't'):
	l = bot.get_database()
	print(len(l))
	print(l)
else:
	print('Bye')
