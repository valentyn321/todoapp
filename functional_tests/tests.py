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
        # and this task was removed from the table coming tasks

        self.browser.find_element_by_xpath("//button[@id='complete_button_1']").click()
        self.wait_for_NO_row_in_list_table('study django at least one hour per day')

        # He decided, that he will do exercise tomorrow, so he log out, and
        # satisfied, he goes back to sleep

        self.browser.find_element_by_xpath("//a[@id='log_out_button']").click()
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('You have been logged out!', header_text)

    

    
    def test_multiple_users(self):
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

        # He doesn't see John's todo-list:
        self.wait_for_NO_row_in_list_table('make 20 push ups')

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

        # But now, he has no time, because he has go to bed, so he tell to
        # his friend Tom to check out this todo list, and go to sleep

        self.browser.find_element_by_xpath("//a[@id='log_out_button']").click()
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('You have been logged out!', header_text)

        # Tom goes to the todo app
        self.browser.get(self.live_server_url)

        # He realized, that he is on log in page
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('Log In!', header_text)
        # Tom haven't got accout, so he clicked on link "Sign Up"
        sign_up_link = self.browser.find_element_by_id('sing_up_link')
        sign_up_link.click()
        # Tom was redirected to sign up page
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertEqual('Plan your life with us!', header_text)

        # He decided to sing up
        username = self.browser.find_element_by_id('id_username')
        username.send_keys('tomas_678')

        email = self.browser.find_element_by_id('id_email')
        email.send_keys('tomas_678@gmail.com')

        password1 = self.browser.find_element_by_id('id_password1')
        password1.send_keys('tester123')

        password2 = self.browser.find_element_by_id('id_password2')
        password2.send_keys('tester123')

        sing_up_button = self.browser.find_element_by_id('sing_up_button')
        sing_up_button.click()

        # He see form, for adding a todo-item, and try to add item
        # "make 20 push ups" in category "Body & Health"

        text = self.browser.find_element_by_id('id_text')
        text.send_keys('make 20 push ups')

        self.browser.find_element_by_xpath("//select[@id='category_select']/option[text()='Body & Health']").click()

        self.browser.find_element_by_xpath("//button[@id='add_button']").click()

        # Then, he see, that his item is in table "Coming tasks":
        header_text = self.browser.find_element_by_tag_name('h3').text
        self.assertIn('Coming tasks:', header_text)

        self.wait_for_row_in_list_table('make 20 push ups')

        # He did his exersices and click on the button "I have already did this",
        # and this task was removed from the table coming tasks
        
        self.browser.find_element_by_xpath("//button[@id='complete_button_4']").click()
        self.wait_for_NO_row_in_list_table('make 20 push ups')

        # He decided to log out, and
        # satisfied, he goes to sleep

        self.browser.find_element_by_xpath("//a[@id='log_out_button']").click()
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn('You have been logged out!', header_text)