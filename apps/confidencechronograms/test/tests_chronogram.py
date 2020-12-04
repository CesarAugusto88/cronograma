from django.test import TestCase
#from django.test.runner import DiscoverRunner

from django.urls import reverse

from confidencechronograms.models import Cliente, Funcionario, Chronogram, Task

class TaskTestCase(TestCase):
    """ A test runner to test without database creation/deletion """
    @classmethod
    def setUpTestData(cls):
        self.chronogram = Chronogram.objects.create(construction="Concreto Armado")
        self.task = Task.objects.create(ident="1")

    def test_verifica_ident_db(self):
        assert Task.objects.all().count() == 1
    
    # def test_task_price(self):
    #     pass

class Status_Code_Tests(TestCase):
    @classmethod
    def test_status_code_login(self):
        response = self.client.get(reverse('login_user'))
        self.assertEqual(response.status_code, 200)
    
    def test_status_code_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_status_code_contact(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)