import car_data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta

class HistoriaPojazdu:

	def __init__(self, rejestracja, vin, rocznik, options=[]):

		self.rejestracja = rejestracja
		self.vin = vin
		self.rocznik = rocznik

		self.url = 'https://historiapojazdu.gov.pl/'
		
		chrome_options = Options()

		for option in options:
			chrome_options.add_argument(option)

		self.driver = webdriver.Chrome(options=chrome_options)

	def closeBrowser(self):

		self.driver.close()

	def search(self):

		date_obj = datetime.strptime(f'0101{self.rocznik}', "%d%m%Y")

		while int(date_obj.strftime('%Y')) == self.rocznik:

			date_str = date_obj.strftime("%d%m%Y")

			self.driver.get(self.url)

			rejestracja = self.driver.find_element_by_id('_historiapojazduportlet_WAR_historiapojazduportlet_:rej')
			rejestracja.clear()
			rejestracja.send_keys(self.rejestracja)

			vin = self.driver.find_element_by_id('_historiapojazduportlet_WAR_historiapojazduportlet_:vin')
			vin.clear()
			vin.send_keys(self.vin)

			data_rejestracji = self.driver.find_element_by_id('_historiapojazduportlet_WAR_historiapojazduportlet_:data')
			data_rejestracji.clear()
			data_rejestracji.send_keys(Keys.HOME)
			data_rejestracji.send_keys(date_str)

			submit = self.driver.find_element_by_xpath('/html/body/main/div/div/div/div/div/div/div/div/div/section[1]/form/fieldset/div/input')
			submit.click()

			if self.driver.page_source.lower().find('oś czasu') > -1:
				return date_str
			else:
				date_obj = date_obj + timedelta(days=1)

		return False

if __name__ == '__main__':

	h = HistoriaPojazdu(car_data.rejestracja, car_data.vin, car_data.rok_rejestracji, ['--incognito'])
	
	print(h.search())

	h.closeBrowser()