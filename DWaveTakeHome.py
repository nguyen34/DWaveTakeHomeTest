import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

class DWaveTakeHome(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Chrome("./chromedriver.exe")

	def test_login_dwave_leap_trial_account(self):
		self.driver.get('https://cloud.dwavesys.com/leap/login/')
		assert "D-Wave Leap Log In" in self.driver.title
		username = self.driver.find_element_by_name("username")
		username.send_keys("nguyenjohnson65@gmail.com")
		password = self.driver.find_element_by_name("password")
		password.send_keys("SenNoKiseki4!")
		self.driver.find_element_by_id("loginFormSubmit").click()
		#Wait Until Page is loaded, afterwards verify all the info in the dashboard-account-container to ensure right user, including First Name, Last Name, Account Type (Trial), Subscription Renewal/Trial Expiry date and Project, if applicable
		wait = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.dashboard-account-container")))
		dashboard = self.driver.find_element_by_css_selector("div.dashboard-account-container")
		assert len(dashboard.find_elements_by_xpath("//*[contains(text(), 'Johnson')]")) > 0
		assert len(dashboard.find_elements_by_xpath("//*[contains(text(), 'Nguyen')]")) > 0
		assert "Trial Plan" in dashboard.find_element_by_class_name("account-type-upgrade-btn-container").text
		assert len(dashboard.find_elements_by_xpath("//*[contains(text(), 'April 19, 2021 (UTC)')]")) > 0

	def test_login_dwave_leap_incorrect_password(self):
		self.driver.get('https://cloud.dwavesys.com/leap/login/')
		assert "D-Wave Leap Log In" in self.driver.title
		username = self.driver.find_element_by_name("username")
		username.send_keys("nguyenjohnson65@gmail.com")
		password = self.driver.find_element_by_name("password")
		password.send_keys("SenNoKiseki4")
		self.driver.find_element_by_id("loginFormSubmit").click()
		#If password is incorrect. Page should reload and it will show an error message
		wait = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.login-error")))
		assert "Please enter a correct email address and password. Note that both fields may be case-sensitive." in self.driver.find_element_by_class_name("login-error").text

	def test_login_dwave_leap_no_password(self):
		self.driver.get('https://cloud.dwavesys.com/leap/login/')
		assert "D-Wave Leap Log In" in self.driver.title
		username = self.driver.find_element_by_name("username")
		username.send_keys("nguyenjohnson65@gmail.com")
		self.driver.find_element_by_id("loginFormSubmit").click()
		#If password does not show. Page should reload with no message
		wait = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "loginFormSubmit")))
		assert "D-Wave Leap Log In" in self.driver.title

	def test_login_dwave_leap_no_username(self):
		self.driver.get('https://cloud.dwavesys.com/leap/login/')
		assert "D-Wave Leap Log In" in self.driver.title
		password = self.driver.find_element_by_name("password")
		password.send_keys("nguyenjohnson65@gmail.com")
		self.driver.find_element_by_id("loginFormSubmit").click()
		#If password does not show. Page should reload with no message
		wait = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "loginFormSubmit")))
		assert "D-Wave Leap Log In" in self.driver.title

	def test_login_dwave_leap_just_click(self):
		self.driver.find_element_by_id("loginFormSubmit").click()
		#If password does not show. Page should reload with no message
		wait = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "loginFormSubmit")))
		assert "D-Wave Leap Log In" in self.driver.title

	def test_login_lockout(self):
		#After running previous tests, account is likely to be locked at this point after so many failed attempts.
		self.driver.get('https://cloud.dwavesys.com/leap/login/')
		assert "D-Wave Leap Log In" in self.driver.title
		username = self.driver.find_element_by_name("username")
		username.send_keys("nguyenjohnson65@gmail.com")
		password = self.driver.find_element_by_name("password")
		password.send_keys("SenNoKiseki4!")
		self.driver.find_element_by_id("loginFormSubmit").click()
		#If password is incorrect. Page should reload and it will show an error message
		wait = WebDriverWait(self.driver, 2)
		assert len(self.driver.find_elements_by_xpath("//*[contains(text(), 'Account Locked Out')]")) > 0

	def tearDown(self):
		self.driver.close()

if __name__ == "__main__":
    unittest.main()