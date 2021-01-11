import random
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Census
from census import views
from voting.models import Voting, Question, Candidate
from base import mods
from base.tests import BaseTestCase
from datetime import date
from django.test import RequestFactory, TestCase


class CensusTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.question = Question(desc='desc')
        self.question.save()

        v1 = Voting(id = 1, name='voting_testing1', question=self.question, escanios=30)
        v1.save()
        
        v2 = Voting(id = 3, name='voting_testing2', question=self.question, escanios=10)
        v2.save()

        user1 = User(id=5, username='voter1', password='test_password')
        user1.save()
        
        user2 = User(id=6, username='voter2', password='test_password')
        user2.save()

        self.census = Census(id=21, voting_id=1, voter_id=5, adscripcion='Colegio1', date=date.today())
        self.census.save()

        c2 = Census(id=22,voting_id=3, voter_id=5, adscripcion='Colegio1', date=date.today())
        c2.save()

        c3 = Census(id=23, voting_id=1, voter_id=6, adscripcion='Colegio2', date=date.today())
        c3.save()

    def tearDown(self):
        super().tearDown()
        self.census = None

    def test_check_vote_permissions(self):
        response = self.client.get('/census/{}/?voter_id={}'.format(1, 2), format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 'Invalid voter')

        response = self.client.get('/census/{}/?voter_id={}'.format(1, 5), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Valid voter')

    def test_list_voting(self):
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'voters': [5, 6]})

    def test_add_new_voters_conflict(self):
        data = {'voting_id': 1, 'voters': [5]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 409)

    def test_add_new_voters(self):
        data = {'voting_id': 2, 'voters': [1,2,3,4], 'adscripcion': 'Colegio 1'}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login(user='admin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(data.get('voters')), 4)

    def test_destroy_voter(self):
        data = {'voters': [1]}
        response = self.client.delete('/census/{}/'.format(1), data, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, len(Census.objects.filter(voter_id=1)))

    def test_model(self):
        c = Census.objects.get(adscripcion = 'Colegio2')
        c.date = date.today
        self.assertEqual(c.voting_id, 1)
        self.assertEqual(c.voter_id, 6)
        self.assertEqual(c.adscripcion, 'Colegio2')
        self.assertEqual(c.date, date.today)
    
    def test_model_functions(self):
        c = self.census
        self.assertEqual(c.voting_name, 'voting_testing1')
        self.assertEqual(c.voting_question, 'desc')
        self.assertEqual(c.voter_username, 'voter1')
    
    def test_all_census(self):
        u = User(username='request_user', password='request_password')
        u.save()
        census = Census.objects.all()
        
        rf = RequestFactory()
        request = rf.get('/census/all_census/')  
        request.user = u
        response = views.all_census(request)
        
        for c in census:
            self.assertContains(response, c)

    def test_group_by_adscripcion(self):
        u = User(username='request_user', password='request_password')
        u.save()
        c1 = Census.objects.get(id=21)
        c2 = Census.objects.get(id=22)
        rf = RequestFactory()
        request = rf.get('/census/group_by_adscripcion/')  
        request.user = u
        response = views.group_by_adscripcion(request,'Colegio1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, c1)
        self.assertContains(response, c2)

    def test_group_by_voting(self):
        u = User(username='request_user', password='request_password')
        u.save()
        c1 = Census.objects.get(id=21)
        c2 = Census.objects.get(id=23)
        rf = RequestFactory()
        request = rf.get('/census/group_by_voting/')  
        request.user = u
        response = views.group_by_voting(request,1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, c1)
        self.assertContains(response, c2)

    def test_group_by_voter(self):
        u = User(username='request_user', password='request_password')
        u.save()
        c1 = Census.objects.get(id=21)
        c2 = Census.objects.get(id=22)
        rf = RequestFactory()
        request = rf.get('/census/group_by_voter/')  
        request.user = u
        response = views.group_by_voter(request,5)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, c1)
        self.assertContains(response, c2)

    def test_group_by_date(self):
        u = User(username='request_user', password='request_password')
        u.save()
        c1 = Census.objects.get(id=21)
        c2 = Census.objects.get(id=22)
        c3 = Census.objects.get(id=23)
        rf = RequestFactory()
        request = rf.get('/census/group_by_date/')  
        request.user = u
        response = views.group_by_date(request,str(date.today()))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, c1)
        self.assertContains(response, c2)
        self.assertContains(response, c3)

    def test_group_by_question(self):
        u = User(username='request_user', password='request_password')
        u.save()
        c1 = Census.objects.get(id=21)
        c2 = Census.objects.get(id=22)
        c3 = Census.objects.get(id=23)
        rf = RequestFactory()
        request = rf.get('/census/group_by_question/')  
        request.user = u
        response = views.group_by_question(request,'desc')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, c1)
        self.assertContains(response, c2)
        self.assertContains(response, c3)

    def test_census_estatistics(self):
        census_per_voters = views.census_per_voters()
        self.assertEquals(census_per_voters['voter1'], 2)
        self.assertEquals(census_per_voters['voter2'], 1)
        escanios = views.escanios()
        self.assertEquals(escanios['voting_testing1'], 30)
        self.assertEquals(escanios['voting_testing2'], 10)
        voters = views.voters()
        self.assertEquals(voters['voting_testing1'], 2)
        self.assertEquals(voters['voting_testing2'], 1)