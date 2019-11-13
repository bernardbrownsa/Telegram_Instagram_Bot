import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import smtplib
import time
import bb_info
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import re

followers = []
random_int = random.randint(0, 4)

def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(bb_info.EMAIL_ADDRESS, bb_info.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(bb_info.EMAIL_ADDRESS, 'bernardbrownsa@gmail.com', message)
        server.quit()
        print('SUCCESS: email sent')
    except:
        print('ERROR: email failed to send')

class InstagramBot():

	def __init__(self, email, password):
		self.browserProfile = webdriver.ChromeOptions()
		self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
		self.browser = webdriver.Chrome('chromedriver.exe', options=self.browserProfile)
		#self.browser = webdriver.Firefox()
		self.email = email
		self.password = password
		self.browser.set_window_size(700, 900)
#IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
	def signIn(self):
		self.browser.get('https://www.instagram.com/accounts/login/')
		time.sleep(5)
		emailInput = self.browser.find_elements_by_css_selector('form input')[0]
		passwordInput = self.browser.find_elements_by_css_selector('form input')[1]

		emailInput.send_keys(self.email)
		passwordInput.send_keys(self.password)
		passwordInput.send_keys(Keys.ENTER)
		time.sleep(2)
#IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
	def like_photo(self, newurl):
		comment_options = ['Looking great!!','Great photo! :)','Love this picture!','Sweet!!','Awesome! :)',
		'Looking Awesome!!','Love This!','Love this!!','This is awesome!','loving this!!','I just checked out your profile and I love it!! Keep up the good work!',
		'I love your profile!',"So cool!",'such a great post!!','this is a great post!!']
		comment_text = random.choice(comment_options)
		time.sleep(1)
		self.browser.get(newurl)
		self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		try:
			time.sleep(random.randint(0, 1))
			like_button = lambda: self.browser.find_element_by_xpath('//span[@aria-label="Like"]').click()
			like_button().click()

		except Exception as e:
			time.sleep(2)
			

#Telegram_Bot
telegram_list = []
final = []
skipped = []

file = open('Desktop/telegram1.txt', 'r')
for line in file:
	if 'www.instagram.com/p/' in line:
		telegram_list.append(line)

for each in telegram_list:
	each = each.replace(' ','')
	if each[0:26] == 'https://www.instagram.com/':
		each = each[0:40]
		final.append(each)
	if each[1:27] == 'https://www.instagram.com/':
		each = each[1:42]
		final.append(each)
	if each[2:28] == 'https://www.instagram.com/':
		final.append(each)
		each = each[2:43]
	if each[3:29] == 'https://www.instagram.com/':
		each = each[3:44]
		final.append(each)
	if each[4:30] == 'https://www.instagram.com/':
		each = each[4:45]
		final.append(each)
	if each[5:31] == 'https://www.instagram.com/':
		each = each[5:46]
		final.append(each)
	if each[6:32] == 'https://www.instagram.com/':
		each = each[6:47]
		final.append(each)
	if each[7:33] == 'https://www.instagram.com/':
		each = each[7:48]
		final.append(each)
	if each[8:34] == 'https://www.instagram.com/':
		each = each[8:49]
		final.append(each)


for each in final:
	print(each)
print('length of telegram_list: ',len(telegram_list))
print('length of full list: ', len(final))


bot = InstagramBot('rhinowallet', '')
send_email('Telegram App Started','Your Telegram app has started and I will send you an email once it is done :)')
#bot = InstagramBot('ItsJamieLizz', '')
bot.signIn()
print('sleeping')
time.sleep(1)
print('done sleeping')
counter = 0
for each in final:
	counter += 1
	try:
		bot.like_photo(each)
	except:
		print('this link is broken')
	print('status: ',counter,'/',len(final))
