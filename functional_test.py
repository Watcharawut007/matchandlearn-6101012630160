from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

from datetime import date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
class FunctionalTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser2 = webdriver.Firefox()
    def tearDown(self):
        self.browser.quit()
        self.browser2.quit()
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('good_subject_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def check_for_row_not_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('good_subject_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertNotIn(row_text, [row.text for row in rows])

    def _a_can_sign_up(self):
        # tiffany wants to be a member so she clicks sign up link
        self.browser.get('http://localhost:8000/')
        time.sleep(1)

        signup_link=self.browser.find_element_by_xpath("//a[@href='/signup/']")
        signup_link.click()
        # She is invited to enter an information
        # She enters username and she notices the username label
        username_label = self.browser.find_element_by_id('Username_label').text
        self.assertEqual('Username',username_label)
        username_box = self.browser.find_element_by_id('username_id')
        username_box.send_keys('Tiffany')
        time.sleep(1)

        # She enters password and she notices the password label
        Password_label = self.browser.find_element_by_id('Password_label').text
        self.assertEqual('Password', Password_label)
        password_box = self.browser.find_element_by_id('password_id')
        password_box.send_keys('Tiffany_password456')
        time.sleep(1)

        # She enters password comfirm and she notices the password comfirm label
        Password_Confirm_label = self.browser.find_element_by_id('Password Confirm_label').text
        self.assertEqual('Password Confirm', Password_Confirm_label)
        password_comfirm_box =self.browser.find_element_by_id('password_confirm_id')
        password_comfirm_box.send_keys('Tiffany_password456')
        time.sleep(1)

        # She enters her first name  and she notices the first name label
        Firstname_label = self.browser.find_element_by_id('First name_label').text
        self.assertEqual('First name', Firstname_label)
        firstname_box = self.browser.find_element_by_id('firstname_id')
        firstname_box.send_keys('Tiffany')
        time.sleep(1)

        # She enters her last name and she notices the last name label
        Lastname_label = self.browser.find_element_by_id('Last name_label').text
        self.assertEqual('Last name', Lastname_label)
        lastname_box = self.browser.find_element_by_id('lastname_id')
        lastname_box.send_keys('Warren')
        time.sleep(1)

        # She enters her collage name and she notices the collage label
        College_label = self.browser.find_element_by_id('College_label').text
        self.assertEqual('College', College_label)
        collage_box = self.browser.find_element_by_id('college_id')
        collage_box.send_keys('Harvard')
        time.sleep(1)

        # She enters her gender and she notices the gender label
        gender_label = self.browser.find_element_by_id('gender_label').text
        self.assertEqual('gender', gender_label)
        gender_select = self.browser.find_element_by_id('id_gender')
        gender_select.send_keys('female')
        time.sleep(1)


        # She enters her email and she notices the email label
        Email_label = self.browser.find_element_by_id('Email_label').text
        self.assertEqual('Email', Email_label)
        email_box =self.browser.find_element_by_id('email_id')
        email_box.send_keys('tiffany456@hotmail.com')
        time.sleep(1)

        # She enters her birthday and she notices the birthday label
        birthday_label = self.browser.find_element_by_id('birthday_label').text
        self.assertEqual('birthday', birthday_label)
        birthday_box = self.browser.find_element_by_id('birthday_id')
        birthday_box.send_keys('03/23/1989')
        time.sleep(1)

        #then she click sign up button
        signup_button = self.browser.find_element_by_id('sighup_button_id')
        self.assertEqual(
            signup_button.get_attribute('type'),
            'submit',
        )

        signup_button.click()
        time.sleep(1)

    def _b_user_can_see_another_profile_and_can_search_tutor(self):

        # Tiffany login to Match and Learn website
        self.browser.get('http://127.0.0.1:8000/login')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('Tiffany')
        password_box.send_keys("Tiffany_password456")
        login_button = self.browser.find_element_by_xpath('//button[@type="submit"]')
        login_button.click()
        time.sleep(2)

        # she go to find her tutor that can teach her math2 so she enter subject into subject field
        tutor_find_box = self.browser.find_element_by_name('tutor_find')
        tutor_find_box.send_keys('Math2')
        time.sleep(2)

        # she clicks at seach button
        seach_button=self.browser.find_element_by_id('search_button')
        seach_button.click()
        time.sleep(2)

        # she see kitsanapong profile and she click it
        kitsanapong_profile= self.browser.find_element_by_name('kitsanapong')
        kitsanapong_profile.click()
        time.sleep(2)

        # she see his name
        name_kitsanapong = self.browser.find_element_by_id('name_user').text
        self.assertEqual('kitsanapong rodjing',name_kitsanapong)
        time.sleep(2)

        # she see his age
        age_kitsanapong = self.browser.find_element_by_id('age_id').text
        self.assertIn('age: 31', age_kitsanapong)
        time.sleep(2)

        # she see his school
        school_kitsanapong = self.browser.find_element_by_id('school_id').text
        self.assertIn('school: kmutnb', school_kitsanapong)
        time.sleep(2)

        # she see his gender
        gender_kitsanapong = self.browser.find_element_by_id('gender').text
        self.assertIn('gender: Male', gender_kitsanapong)
        time.sleep(2)

        # she see his expertise subject and know his expertise subject is math2
        expertise_kitsanapong=self.browser.find_element_by_xpath('//h3[text()="math2"]').text
        self.assertIn('math2',expertise_kitsanapong)
        time.sleep(2)

    def _c_watch_personal_profile_and_add_or_remove_expertise_subject(self):
        # tiffany wants to add her good subject so she go to match and learn website
        self.browser.get('http://127.0.0.1:8000/login')
        time.sleep(2)
        # tiffany login
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('Tiffany')
        password_box.send_keys("Tiffany_password456")
        time.sleep(2)
        login_button = self.browser.find_element_by_xpath('//button[@type="submit"]')
        login_button.click()
        time.sleep(2)

        # she clicks at profile button
        personal_button = self.browser.find_element_by_id('personal_profile_id')
        personal_button.click()
        time.sleep(1)

        # she notices the header mention Add your expertise subject
        header_text = self.browser.find_element_by_xpath('//h2[text()="Add your expertise subject"]').text
        self.assertEqual(header_text,'Add your expertise subject')
        time.sleep(1)

        # she enter her expertise subjects
        inputbox = self.browser.find_element_by_id('subject_good_id')

        # she types "english" into a text box
        inputbox.send_keys('english')
        time.sleep(2)

        # she notices add button and she clicks it
        addbutton = self.browser.find_element_by_name('add_button')
        addbutton.click()
        time.sleep(2)
        self.check_for_row_in_list_table('1: english')

        # she types "computer" into a text box
        inputbox = self.browser.find_element_by_id('subject_good_id')
        inputbox.send_keys('computer')
        time.sleep(2)
        # she notices add button and she clicks it
        addbutton = self.browser.find_element_by_name('add_button')
        addbutton.click()
        time.sleep(2)
        self.check_for_row_in_list_table('2: computer')

        # she types "physic" into a text box
        inputbox = self.browser.find_element_by_id('subject_good_id')
        inputbox.send_keys('physic')
        time.sleep(2)

        # she notices add button and she clicks it
        addbutton = self.browser.find_element_by_name('add_button')
        addbutton.click()
        time.sleep(2)
        self.check_for_row_in_list_table('3: physic')

        # she notices checkbox at the orther her expertise subject and remove button
        remove_button = self.browser.find_element_by_name('remove_button')
        english_check_box=self.browser.find_element_by_id('english')
        physic_check_box = self.browser.find_element_by_id('physic')
        # she forget that she do not good at english and physic then she clicks at english check box and click remove it
        english_check_box.click()
        time.sleep(2)
        physic_check_box.click()
        time.sleep(2)
        remove_button.click()
        time.sleep(2)

        # she do not see subjects that she remove
        self.check_for_row_not_in_list_table('1: english')
        self.check_for_row_not_in_list_table('3: physic')
        time.sleep(2)

        # she see computer subject that she like
        self.check_for_row_in_list_table('1: computer')
        time.sleep(1)


    def _d_match_other_user(self):
        # Tiffany login to Match and Learn website
        self.browser.get('http://127.0.0.1:8000/login')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('Tiffany')
        password_box.send_keys("Tiffany_password456")
        time.sleep(2)
        login_button = self.browser.find_element_by_xpath('//button[@type="submit"]')
        login_button.click()
        time.sleep(2)

        # she go to find her tutor that can teach her math2 so she enter subject into subject field
        tutor_find_box = self.browser.find_element_by_name('tutor_find')
        tutor_find_box.send_keys('Math2')
        time.sleep(2)

        # she clicks at seach button
        seach_button = self.browser.find_element_by_id('search_button')
        seach_button.click()
        time.sleep(2)

        # she see kitsanapong profile and she click it
        kitsanapong_profile = self.browser.find_element_by_name('kitsanapong')
        kitsanapong_profile.click()
        time.sleep(2)

        # she see match button
        match_button=self.browser.find_element_by_name('match')
        self.assertEqual(match_button.text,'MATCH')
        time.sleep(2)

        # she want to tell something to him before matching
        tell_something_about_you=self.browser.find_element_by_name('text_request')
        tell_something_about_you.send_keys('I do not good at math2 so can you teach me?')
        time.sleep(2)

        # she clicks it because she want him to be her tutor
        match_button.click()
        time.sleep(2)

        # she see match button
        match_button = self.browser.find_element_by_name('Unmatched')
        self.assertEqual(match_button.text, 'UNMATCHED')
        time.sleep(2)

    def _e_accept_match_request(self):
        #kitsanapong login
        self.browser.get('http://127.0.0.1:8000/login')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('watcharawut007')
        password_box.send_keys("tongu4590")
        time.sleep(2)
        login_button = self.browser.find_element_by_xpath('//button[@type="submit"]')
        login_button.click()
        time.sleep(2)

        # he see a notification maybe someone was sent student request to him
        notifycount = self.browser.find_element_by_name('value_notificate').text
        self.assertIn(notifycount, '1')
        time.sleep(2)

        # then, he click on student request page
        student_request_page = self.browser.find_element_by_name('Match request')
        student_request_page.click()
        time.sleep(2)

        # he saw Tiffany is the one who was sent request to him

        # he saw Tiffany name
        tiffany_info_name = self.browser.find_element_by_xpath('//h1[text()="Tiffany Warren"]')
        self.assertIn(tiffany_info_name.text, 'Tiffany Warren')
        time.sleep(2)

        # he saw Tiffany age
        tiffany_info_age = self.browser.find_element_by_xpath('//p[text()=" age: 31"]')
        self.assertIn(tiffany_info_age.text, ' age: 31')
        time.sleep(3)

        #he click on tiffany request
        tiffany_box = self.browser.find_element_by_name('Tiffany_request')
        tiffany_box.click()
        time.sleep(2)

        # he see a short message I do not good at math2 so can you teach me?
        tiffany_message = self.browser.find_element_by_xpath('//h3[text()="Tiffany leave a short message for you : I do not good at math2 so can you teach me?"]')
        self.assertEqual(tiffany_message.text,'Tiffany leave a short message for you : I do not good at math2 so can you teach me?')
        time.sleep(2)

        #he see that he can choose to accept request or decline request then he choose accept
        accept_button = self.browser.find_element_by_id('accept_button_id')
        time.sleep(2)
        accept_button.click()
        time.sleep(2)

        # he go to student and tutor list to see tiffany
        student_tutor_button = self.browser.find_element_by_name('Students and Tutor list')
        student_tutor_button.click()
        time.sleep(2)

        # he go to see tiffany profile
        tiffany_box = self.browser.find_element_by_id('Tiffany')
        tiffany_box.click()
        time.sleep(2)

        # he saw that now he's match with Tiffany.
        # He can now choose to unmatched but he don't want to do it.
        unmatch_button=self.browser.find_element_by_name('unmatch')
        self.assertEqual(unmatch_button.text,'UNMATCHED')
        time.sleep(2)


    #COMMENT
    def _f_an_comment_to_another_user_who_matched_with_him_and_can_delete_it(self):
        # watcharawut login to Match and Learn website
        self.browser.get('http://127.0.0.1:8000/login')
        username_box = self.browser.find_element_by_name('username')  # user see the username field
        password_box = self.browser.find_element_by_name('password')  # user see the password field
        username_box.send_keys('watcharawut009')
        password_box.send_keys("tongu20068")
        time.sleep(2)
        # He notices the login button and he click it
        login_button = self.browser.find_element_by_tag_name('button')
        login_button.click()
        time.sleep(2)

        # He go to student and tutor list
        student_and_tutor_list_btn = self.browser.find_element_by_id('tutor_student_list_id')
        student_and_tutor_list_btn.click()
        time.sleep(2)

        # He click on kitsanapong profile
        kitsanapong_profile = self.browser.find_element_by_id('kitsanapong')
        kitsanapong_profile.click()
        time.sleep(2)

        # He enter comment  "kitsanapong is a good student"
        comment = self.browser.find_element_by_id('id_comment')
        comment.send_keys("kitsanapong is a good student")
        time.sleep(2)

        # So, He give score to kitsanapong 4 star
        self.browser.find_element_by_xpath("//select[@name='star']/option[text()='4']").click()
        time.sleep(2)

        # He submit comment
        comment_button = self.browser.find_element_by_id('comment_submit_id')
        comment_button.click()
        time.sleep(2)

        # He saw comment that he posted
        comment_text = self.browser.find_element_by_id('watcharawut').text
        self.assertEqual(comment_text, "Comment : kitsanapong is a good student")
        time.sleep(2)

        # He thinks he want to delete his comment maybe he change his mine
        comment_delete_button = self.browser.find_element_by_id('watcharawut_delete_comment')
        comment_delete_button.click()
        time.sleep(2)

        # he try to count amount comment that he saw in the kitsanapong profile
        amount_comment = len(self.browser.find_elements_by_id('watcharawut'))

        # amount comment equal 0
        self.assertEqual(0, amount_comment)
        time.sleep(2)

    def _g_user_can_not_delete_another_user_comment(self):
        # kitsanapong login to Match and Learn website
        self.browser.get('http://127.0.0.1:8000/login')
        username_box = self.browser.find_element_by_name('username')  # user see the username field
        password_box = self.browser.find_element_by_name('password')  # user see the password field
        username_box.send_keys('watcharawut007')
        password_box.send_keys("tongu4590")
        time.sleep(2)

        # He notices the login button and he click it
        login_button = self.browser.find_element_by_tag_name('button')
        login_button.click()
        time.sleep(2)

        # He go to student and tutor list
        student_and_tutor_list_btn = self.browser.find_element_by_id('tutor_student_list_id')
        student_and_tutor_list_btn.click()
        time.sleep(2)

        # He click on watcharawut  profile
        watcharwaut_profile = self.browser.find_element_by_id('watcharawut')
        watcharwaut_profile.click()
        time.sleep(2)

        # He enter comment  "i can not understand everything that he taught me"
        comment = self.browser.find_element_by_id('id_comment')
        comment.send_keys("i can not understand everything that he taught me")
        time.sleep(2)

        # So, He give score to watcharawut 2 star
        self.browser.find_element_by_xpath("//select[@name='star']/option[text()='2']").click()
        time.sleep(2)

        # He submit comment
        comment_button = self.browser.find_element_by_id('comment_submit_id')
        comment_button.click()
        time.sleep(2)

        # He saw comment that he posted
        comment_text = self.browser.find_element_by_id('kitsanapong').text
        self.assertEqual(comment_text, "Comment : i can not understand everything that he taught me")
        time.sleep(2)

        # He saw Theeraphat comment that he thinks that it is lie and he try to delete it
        another_comment = self.browser.find_element_by_id('Theeraphat').text
        self.assertEqual(another_comment, "Comment : he is good teacher")
        time.sleep(2)

        # He try to find remove button on the theeraphat comment
        remove_comment_button = len(self.browser.find_elements_by_id('Theeraphat_delete_comment'))

        # He can not find
        self.assertEqual(0, remove_comment_button)


    def _h_user_can_chat_to_each_other(self):

        # Tiffany and Kitsanapong go to website Match and Learn and login
        self.browser.get('http://127.0.0.1:8000/login')
        self.browser2.get('http://127.0.0.1:8000/login')
        time.sleep(2)

        #kitsanapong login
        username_box = self.browser.find_element_by_id('id_username')
        username_box.send_keys('watcharawut007')
        password_box = self.browser.find_element_by_id('id_password')
        password_box.send_keys("tongu4590")
        time.sleep(2)
        login_button = self.browser.find_element_by_tag_name('button')
        login_button.click()
        time.sleep(2)

        # Tiffany login
        username_box = self.browser2.find_element_by_id('id_username')
        username_box.send_keys('Tiffany')
        password_box = self.browser2.find_element_by_id('id_password')
        password_box.send_keys("Tiffany_password456")
        time.sleep(2)
        login_button = self.browser2.find_element_by_tag_name('button')
        login_button.click()
        time.sleep(2)

        #kitsanapong go to tutor and student list
        kitsanapong_tutor_student_list = self.browser.find_element_by_id('tutor_student_list_id')
        kitsanapong_tutor_student_list.click()
        time.sleep(2)

        # Tiffany go to tutor and student list
        tiffany_tutor_student_list = self.browser2.find_element_by_id('tutor_student_list_id')
        tiffany_tutor_student_list.click()
        time.sleep(2)

        #they see chat room button then they clicks to chat each orther
        self.browser.get('http://127.0.0.1:8000/chat/Tiffany_watcharawut007/')
        time.sleep(2)
        self.browser2.get('http://127.0.0.1:8000/chat/Tiffany_watcharawut007/')
        time.sleep(2)

        # Kitsanapong type "Hello, I am Kitsanapong.What is your name?" to Tiffany
        message_input_field = self.browser.find_element_by_id('chat-message-input')
        time.sleep(3)
        message_input_field.send_keys('Hello, I am Kitsanapong.What is your name?')
        time.sleep(2)
        submit_messange_button = self.browser.find_element_by_id('chat-message-submit')
        submit_messange_button.click()
        time.sleep(2)

        # Kitsanapong see his message that he was sent on right side
        message = self.browser.find_element_by_id('chat-log')
        self.assertIn('Hello, I am Kitsanapong.What is your name?', message.get_attribute('value'))
        time.sleep(2)

        # Tiffany get message from Kitsanapong on the left side
        messagefrom_Kitsanapong = self.browser2.find_element_by_id('chat-log2')
        self.assertIn('Hello, I am Kitsanapong.What is your name?', messagefrom_Kitsanapong.get_attribute('value'))
        time.sleep(2)

        # Tiffany send message to Kitsanapong "my name is Tiffany nice to meet you"
        messange_input_field = self.browser2.find_element_by_id('chat-message-input')
        messange_input_field.send_keys('my name is Tiffany nice to meet you')
        time.sleep(2)
        submit_message_button = self.browser2.find_element_by_id('chat-message-submit')
        submit_message_button.click()
        time.sleep(2)


        # Tiffany see her message that she was sent on right side
        message_tiffany = self.browser2.find_element_by_id('chat-log')
        self.assertIn('my name is Tiffany nice to meet you', message_tiffany.get_attribute('value'))
        time.sleep(2)

        # Kitsanapong get message from tiffany on the left side
        message_receive_from_nattakrit = self.browser.find_element_by_id('chat-log2')
        self.assertIn('my name is Tiffany nice to meet you', message_receive_from_nattakrit.get_attribute('value'))
        time.sleep(2)


    def _i_user_unmatched(self):
        # kitsanapong login
        self.browser.get('http://127.0.0.1:8000/login')
        username_box = self.browser.find_element_by_id('id_username')
        password_box = self.browser.find_element_by_id('id_password')
        username_box.send_keys('watcharawut007')
        password_box.send_keys("tongu4590")
        time.sleep(2)
        login_button = self.browser.find_element_by_xpath('//button[@type="submit"]')
        login_button.click()

        # then, he click on student tutor list page
        tutor_student_page = self.browser.find_element_by_id('tutor_student_list_id')
        tutor_student_page.click()
        time.sleep(2)

        #he see a tiffany in student tutor list page
        tiffany_box =self.browser.find_element_by_id("Tiffany")
        tiffany_box.click()
        time.sleep(2)

        # he see a unmatched button then he click it
        unmatch_button =self.browser.find_element_by_name("unmatch")
        self.assertEqual("UNMATCHED",unmatch_button.text)
        unmatch_button.click()
        time.sleep(2)

        # he do not see a tiffany in page
        studentlist = self.browser.find_elements_by_id("Tiffany")
        self.assertEqual(len(studentlist),0)
        time.sleep(2)

    def _j_user_check_his_age_and_another_user(self):
        if datetime.now().year == 2020:
            self.browser.get('http://127.0.0.1:8000/login') #user go to login page
            username_box = self.browser.find_element_by_name('username')#user see the username field
            password_box = self.browser.find_element_by_name('password')#user see the password field

            # user enter his username/password
            username_box.send_keys('watcharawut009')
            password_box.send_keys("tongu20068")

            #user notices the login button and he click it
            login_button = self.browser.find_element_by_tag_name('button')
            login_button.click()
            time.sleep(2)

            # user notices the Profile button and he click it
            profile_button = self.browser.find_element_by_id('personal_profile_id')
            profile_button.click()
            time.sleep(1)

            # user notices his age
            age_user = self.browser.find_element_by_id('age_id').text
            self.assertIn(age_user,'age: 20')

            # user notices his birthday
            birthday_user = self.browser.find_element_by_id('birthday_id').text
            self.assertIn(birthday_user,'birthday: April 24, 2000')
            time.sleep(2)

            # user wants to back to home page
            back_to_home_button = self.browser.find_element_by_id('home')
            back_to_home_button.click()
            time.sleep(1)

            # user wants to find tutor to teach math2
            search_box = self.browser.find_element_by_name('tutor_find')
            search_box.send_keys('math2')
            time.sleep(1)

            # user notices the search button and he click it
            search_button = self.browser.find_element_by_id('search_button')
            search_button.click()
            time.sleep(2)

            # user notices the first tutor that he found and he want to see his profile
            search_result = self.browser.find_element_by_id('1')
            search_result.click()

            # user notices his age
            age_anotheruser = self.browser.find_element_by_id('age_id').text
            self.assertIn(age_anotheruser, 'age: 31')

            # user notices his birthday
            birthday_user = self.browser.find_element_by_id('birthday_id').text
            self.assertIn(birthday_user, 'birthday: April 25, 1989')
            time.sleep(2)


    def test_k_user_check_his_age_and_another_user_when_1_year_past(self):
        if  datetime.now().year == 2021:
            self.browser.get('http://127.0.0.1:8000/login')  # user go to login page
            username_box = self.browser.find_element_by_name('username')  # user see the username field
            password_box = self.browser.find_element_by_name('password')  # user see the password field

            # user enter his username/password
            username_box.send_keys('watcharawut009')
            password_box.send_keys("tongu20068")

            # user notices the login button and he click it
            login_button = self.browser.find_element_by_tag_name('button')
            login_button.click()
            time.sleep(2)

            # user notices the Profile button and he click it
            profile_button = self.browser.find_element_by_id('personal_profile_id')
            profile_button.click()
            time.sleep(1)

            # user notices his age
            age_user = self.browser.find_element_by_id('age_id').text
            self.assertIn(age_user, 'age: 21')

            # user notices his birthday
            birthday_user = self.browser.find_element_by_id('birthday_id').text
            self.assertIn(birthday_user, 'birthday: April 24, 2000')
            time.sleep(2)

            # user wants to back to home page
            back_to_home_button = self.browser.find_element_by_id('home')
            back_to_home_button.click()
            time.sleep(1)

            # user wants to find tutor to teach math2
            search_box = self.browser.find_element_by_name('tutor_find')
            search_box.send_keys('math2')
            time.sleep(1)

            # user notices the search button and he click it
            search_button = self.browser.find_element_by_id('search_button')
            search_button.click()
            time.sleep(2)

            # user notices the first tutor that he found and he want to see his profile
            search_result = self.browser.find_element_by_id('1')
            search_result.click()

            # user notices his age
            age_anotheruser = self.browser.find_element_by_id('age_id').text
            self.assertIn(age_anotheruser, 'age: 32')

            # user notices his birthday
            birthday_user = self.browser.find_element_by_id('birthday_id').text
            self.assertIn(birthday_user, 'birthday: April 25, 1989')
            time.sleep(2)



if __name__ == '__main__':
    unittest.main(warnings='ignore')
