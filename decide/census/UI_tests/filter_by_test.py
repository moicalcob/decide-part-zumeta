from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from base.tests import BaseTestCase
from django.contrib.auth.models import User
from census.models import Census
from voting.models import Voting, Question
from datetime import date

class TestGroupingbyvotingtest(StaticLiveServerTestCase):
  
    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()
        options = webdriver.ChromeOptions()
        options.headless = False
        self.driver = webdriver.Chrome(options=options)  

        question = Question(desc='desc')
        question.save()

        v1 = Voting(id = 1, name='voting_testing1', question=question)
        v1.save()
    
        v2 = Voting(id = 3, name='voting_testing2', question=question)
        v2.save()

        user1 = User(id=5, username='voter1', password='test_password')
        user1.save()
    
        user2 = User(id=6, username='voter2', password='test_password')
        user2.save()

        c1 = Census(id=21, voting_id=1, voter_id=5, adscripcion='Colegio1', date=date.today())
        c1.save()

        c2 = Census(id=22,voting_id=3, voter_id=5, adscripcion='Colegio1', date=date.today())
        c2.save()

        super().setUp()
  
    def tearDown(self):
        super().tearDown()
    
        self.driver.quit()
        self.base.tearDown()
    
    def filter_by_test(self):
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("qwerty",Keys.ENTER)

        self.driver.get(f'{self.live_server_url}/census/admin/')
        self.driver.find_element(By.ID, "q").click()
        self.driver.find_element(By.ID, "q").send_keys("Colegio1")
        self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(2)").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".filas-tabla:nth-child(1) > td:nth-child(3)").text == "Colegio1"
        assert self.driver.find_element(By.CSS_SELECTOR, ".filas-tabla:nth-child(2) > td:nth-child(3)").text == "Colegio1"