from django.test import LiveServerTestCase
from django.core.management import call_command

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time


class NewVisitorClass(LiveServerTestCase):
    
    MAX_WAIT = 10
    
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path=r'geckodriver')
        call_command('loaddata', 'categories.json', verbosity=0)

    def tearDown(self):
        self.browser.quit()

    # Be carefull there are wait_for_row_in_list_table and wait_for_NO_row_in_list_table 

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('ul_coming')
                rows = table.find_elements_by_tag_name('span')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for_NO_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('ul_coming')
                rows = table.find_elements_by_tag_name('span')
                self.assertNotIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def test_for_one_user(self):
        # John has heard about a cool new online to-do app. He wanna
        # to try it.
        self.browser.get(self.live_server_url)

        # He notices the page title mention to-do lists
        self.assertIn('ToDo', self.browser.title)
        # Also, he realized, that he is on log in page
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Log In!', header_text)
        # John haven't got accout, so he clicked on link "Sign Up"
        sign_up_link = self.browser.find_element_by_id('sing_up_link')
        sign_up_link.click()
        # John was redirected to sign up page
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertEqual('Plan your life with us!', header_text)

        # He decided to sing up
        username = self.browser.find_element_by_id('id_username')
        username.send_keys('john22')

        email = self.browser.find_element_by_id('id_email')
        email.send_keys('john22@gmail.com')

        password1 = self.browser.find_element_by_id('id_password1')
        password1.send_keys('tester123')

        password2 = self.browser.find_element_by_id('id_password2')
        password2.send_keys('tester123')

        sing_up_button = self.browser.find_element_by_id('sing_up_button')
        sing_up_button.click()

        # And try to login
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Log In!', header_text)

        username = self.browser.find_element_by_id('id_username')
        username.send_keys('john22')

        password = self.browser.find_element_by_id('id_password')
        password.send_keys('tester123')

        log_in_button = self.browser.find_element_by_id('log_in_button')
        log_in_button.click()

        # He see form, for adding a todo-item, and try to add item
        # "study django at least one hour per day" in category "Study"

        text = self.browser.find_element_by_id('id_text')
        text.send_keys('study django at least one hour per day')

        self.browser.find_element_by_xpath("//select[@id='category_select']/option[text()='Study']").click()

        self.browser.find_element_by_xpath("//button[@id='add_button']").click()

        # Then, he see, that his item is in table "Coming tasks":
        header_text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('Coming tasks:', header_text)

        self.wait_for_row_in_list_table('study django at least one hour per day')

        # Then he wanna to add one more item in category "Sport":
        # make 20 push ups

        text = self.browser.find_element_by_id('id_text')
        text.send_keys('make 20 push ups')

        self.browser.find_element_by_xpath("//select[@id='category_select']/option[text()='Body & Health']").click()

        self.browser.find_element_by_xpath("//button[@id='add_button']").click()

        # Then, he see, that his items are in table "Coming tasks":
        header_text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('Coming tasks:', header_text)

        self.wait_for_row_in_list_table('study django at least one hour per day')
        self.wait_for_row_in_list_table('make 20 push ups')

        # He studied for one hour and click on the button "I have already did this",
        # and this task was removed from the page

        self.browser.find_element_by_xpath("//button[@id='complete_button_1']").click()
        self.wait_for_NO_row_in_list_table('study django at least one hour per day')

        # He decided, that he will do exercise tomorrow, so he log out, and
        # satisfied, he goes back to sleep

        self.browser.find_element_by_xpath("//a[@id='log_out_button']").click()
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('You have been logged out!', header_text)

    

    
    # def test_multiple_users(self):
    #     # Edith starts a new to-do list
    #     self.browser.get(self.live_server_url)
    #     inputbox = self.browser.find_element_by_id('id_new_item')
    #     inputbox.send_keys("1: Buy peacock feathers")
    #     inputbox.send_keys(Keys.ENTER)
    #     self.wait_for_row_in_list_table('1: Buy peacock feathers')

    #     # She notices that her list has a unique URL
    #     edith_list_url = self.browser.current_url
    #     self.assertRegex(edith_list_url, '/lists/.+')

    #     # Now a new user, Francis, comes along to the site.

    #     ## We use a new browser session to make sure that no information
    #     ## of Edith's is coming through from cookies etc
    #     self.browser.quit()
    #     self.browser = webdriver.Firefox(executable_path=r'/home/valentyn/Documents/tdd-book/code/geckodriver')

    #     # Francis visits the home page.  There is no sign of Edith's
    #     # list
    #     self.browser.get(self.live_server_url)
    #     page_text = self.browser.find_element_by_tag_name('body').text
    #     self.assertNotIn('Buy peacock feathers', page_text)
    #     self.assertNotIn('make a fly', page_text)

    #     # Francis starts a new list by entering a new item. He
    #     # is less interesting than Edith...
    #     inputbox = self.browser.find_element_by_id('id_new_item')
    #     inputbox.send_keys('1: Buy milk')
    #     inputbox.send_keys(Keys.ENTER)
    #     self.wait_for_row_in_list_table('1: Buy milk')

    #     # Francis gets his own unique URL
    #     francis_list_url = self.browser.current_url
    #     self.assertRegex(francis_list_url, '/lists/.+')
    #     self.assertNotEqual(francis_list_url, edith_list_url)

    #     # Again, there is no trace of Edith's list
    #     page_text = self.browser.find_element_by_tag_name('body').text
    #     self.assertNotIn('Buy peacock feathers', page_text)
    #     self.assertIn('Buy milk', page_text)

    #     # Satisfied, they both go back to sleep

