from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import InsuranceAgent, Contacts
from .models.insurance_client import InsuranceClient
from .models.company_branch import CompanyBranch


class CompanyBranchModelTest(TestCase):
    def test_create_company_branch(self):
        branch = CompanyBranch.objects.create(
            name='Branch A',
            address='123 Main Street',
            phone_number='555-1234'
        )
        self.assertEqual(branch.name, 'Branch A')
        self.assertEqual(branch.address, '123 Main Street')
        self.assertEqual(branch.phone_number, '555-1234')


class ContactsModelTest(TestCase):
    def test_create_contacts(self):
        # Assuming InsuranceAgent is defined somewhere
        agent = InsuranceAgent.objects.create(name='Agent A')
        contacts = Contacts.objects.create(
            employee_image='path/to/image.jpg',
            agent=agent,
            position='Manager',
            email='test@example.com'
        )
        self.assertEqual(contacts.position, 'Manager')
        self.assertEqual(contacts.email, 'test@example.com')


class InsuranceClientModelTest(TestCase):
    def test_create_insurance_client(self):
        # Assuming User is defined somewhere
        user = User.objects.create(username='testuser')
        client = InsuranceClient.objects.create(
            user=user,
            name='John',
            surname='Doe',
            second_name='Smith',
            age=25,
            address='456 Elm Street',
            phone_number='555-5678'
        )
        self.assertEqual(client.name, 'John')
        self.assertEqual(client.surname, 'Doe')
        self.assertEqual(client.second_name, 'Smith')
        self.assertEqual(client.age, 25)
        self.assertEqual(client.address, '456 Elm Street')
        self.assertEqual(client.phone_number, '555-5678')

    # def test_invalid_age(self):
    #     user = User.objects.create(username='testuser')
    #     with self.assertRaises(ValidationError):
    #         InsuranceClient.objects.create(
    #             user=user,
    #             name='John',
    #             surname='Doe',
    #             second_name='Smith',
    #             age=15,  # Invalid age
    #             address='456 Elm Street',
    #             phone_number='555-5678'
    #         )
