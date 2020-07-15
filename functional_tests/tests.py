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

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
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



    #     # She is invited to enter a to-do item straight away
    #     inputbox = self.browser.find_element_by_id('id_new_item')
    #     self.assertEqual(
    #         inputbox.get_attribute('placeholder'),
    #         'Enter here, what you have to do...'
    #     )

    #     # She types "Buy peacock feathers" into a text box (Edith's hobby
    #     # is tying fly-fishing lures)
    #     inputbox.send_keys('1: Buy peacock feathers')

    #     # When she hits enter, the page updates, and now the page lists
    #     # "1: Buy peacock feathers" as an item in a to-do list
    #     inputbox.send_keys(Keys.ENTER)

    #     self.wait_for_row_in_list_table('1: Buy peacock feathers')
    #     # There is still a text box inviting her to add another item. She
    #     # enters "Use peacock feathers to make a fly" (Edith is very methodical)
    #     inputbox = self.browser.find_element_by_id('id_new_item')
    #     inputbox.send_keys('2: Use peacock feathers to make a fly')
    #     inputbox.send_keys(Keys.ENTER)
        

    #     # The page updates again, and now shows both items on her list
    #     self.wait_for_row_in_list_table('1: Buy peacock feathers')
    #     self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        

    #     # Edith wonders whether the site will remember her list. Then she sees
    #     # that the site has generated a unique URL for her -- there is some
    #     # explanatory text to that effect.
    

    #     # She visits that URL - her to-do list is still there.

    #     # Satisfied, she goes back to sleep
    
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

