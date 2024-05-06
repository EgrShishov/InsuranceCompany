from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from ..models import InsuranceAgent, InsuranceContract, InsuranceObject,\
    InsuranceType, InsuranceClient, CompanyBranch, Review, News
from ..views import index_view
from unittest.mock import patch
from ..forms.authorization import RegistrationForm, LoginForm
from ..forms.make_review import MakeReview
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
import datetime
from ..views.accounts import custom_login, logout_view, register
from ..views.accounts import superuser_profile_view
from ..views.accounts import employee_profile_view, user_profile_view
from ..views.reviews import create
from ..views.news import home


class InsuranceAgentViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='12345')
        permission_add = Permission.objects.get(name='Can add insurance agent')
        permission_change = Permission.objects.get(name='Can change insurance agent')
        permission_delete = Permission.objects.get(name='Can delete insurance agent')
        self.user.user_permissions.add(permission_add, permission_change, permission_delete)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_create_view(self):
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')

        data = {
            'name': 'John',
            'surname': 'Doe',
            'second_name': 'Smith',
            'age': 30,
            'address': '123 Main St',
            'branch_name': 'Branch A',
            'phone_number': '+375 (29) 123-45-67'
        }
        response = self.client.post(reverse('create'), data)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(InsuranceAgent.objects.filter(name='John').exists())

    def test_edit_view(self):
        agent = InsuranceAgent.objects.create(name='Jane', surname='Doe', second_name='Smith', age=25,
                                              address='456 Elm St', branch_name='Branch B', phone_number='+375 (29) 987-65-43')

        response = self.client.get(reverse('edit', kwargs={'id': agent.id}))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('edit', kwargs={'id': agent.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit.html')

        data = {
            'name': 'Jane Updated',
            'surname': 'Doe',
            'second_name': 'Smith',
            'age': 25,
            'address': '456 Elm St',
            'branch_name': 'Branch B',
            'phone_number': '+375 (29) 987-65-43'
        }
        response = self.client.post(reverse('edit', kwargs={'id': agent.id}), data)
        self.assertEqual(response.status_code, 302)

        updated_agent = InsuranceAgent.objects.get(id=agent.id)
        self.assertEqual(updated_agent.name, 'Jane Updated')

    def test_delete_view(self):
        agent = InsuranceAgent.objects.create(name='Jane', surname='Doe', second_name='Smith', age=25,
                                              address='456 Elm St', branch_name='Branch B', phone_number='+375 (29) 987-65-43')

        response = self.client.get(reverse('delete', kwargs={'id': agent.id}))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('delete', kwargs={'id': agent.id}))
        self.assertEqual(response.status_code, 302)

        self.assertFalse(InsuranceAgent.objects.filter(id=agent.id).exists())


class InsuranceContractViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='12345')
        permission_add = Permission.objects.get(name='can_add_insurancecontract')
        permission_change = Permission.objects.get(name='can_change_insurancecontract')
        permission_delete = Permission.objects.get(name='can_delete_insurancecontract')
        self.user.user_permissions.add(permission_add, permission_change, permission_delete)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'insurance_contract/index.html')

    def test_create_view_get(self):
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'insurance_contract/create.html')

    def test_create_view_post(self):
        self.client.login(username='testuser', password='12345')

        data = {
            'branch_name': 'Branch A',
            'insurance_type': 'Type A',
            'tariff_rate': 0.05,
            'sum': 1000.0
        }
        response = self.client.post(reverse('create'), data)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(InsuranceContract.objects.filter(branch_name='Branch A').exists())

    def test_edit_view_get(self):
        contract = InsuranceContract.objects.create(branch_name='Branch A', insurance_type='Type A',
                                                     tariff_rate=0.05, sum=1000.0)

        response = self.client.get(reverse('edit', kwargs={'id': contract.id}))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('edit', kwargs={'id': contract.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'insurance_contract/edit.html')

    def test_edit_view_post(self):
        contract = InsuranceContract.objects.create(branch_name='Branch A', insurance_type='Type A',
                                                     tariff_rate=0.05, sum=1000.0)
        self.client.login(username='testuser', password='12345')
        data = {
            'branch_name': 'Branch B',
            'insurance_type': 'Type B',
            'tariff_rate': 0.07,
            'sum': 2000.0
        }
        response = self.client.post(reverse('edit', kwargs={'id': contract.id}), data)
        self.assertEqual(response.status_code, 302)

        updated_contract = InsuranceContract.objects.get(id=contract.id)
        self.assertEqual(updated_contract.branch_name, 'Branch B')

    def test_delete_view(self):
        contract = InsuranceContract.objects.create(branch_name='Branch A', insurance_type='Type A',
                                                     tariff_rate=0.05, sum=1000.0)

        response = self.client.get(reverse('delete', kwargs={'id': contract.id}))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='12345')

        response = self.client.get(reverse('delete', kwargs={'id': contract.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(InsuranceContract.objects.filter(id=contract.id).exists())


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        permission_view = Permission.objects.get(name='Can view insurance type')
        self.user.user_permissions.add(permission_view)
        self.insurance_type1 = InsuranceType.objects.create(name='Type A', description='Description A', percentage=0.05)
        self.insurance_type2 = InsuranceType.objects.create(name='Type B', description='Description B', percentage=0.1)

    def test_index_view_without_search_and_sorting(self):
        request = self.factory.get(reverse('index'))
        request.user = self.user
        response = index_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'insurance/insurance_types.html')
        self.assertQuerysetEqual(response.context_data['types'], InsuranceType.objects.all())

    def test_index_view_with_search(self):
        request = self.factory.get(reverse('index') + '?search=Type A')
        request.user = self.user
        response = index_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'insurance/insurance_types.html')
        self.assertQuerysetEqual(response.context_data['types'], InsuranceType.objects.filter(name__icontains='Type A'))

    def test_index_view_sort_by_name(self):
        request = self.factory.get(reverse('index') + '?sort_by=name')
        request.user = self.user
        response = index_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'insurance/insurance_types.html')
        self.assertQuerysetEqual(response.context_data['types'], InsuranceType.objects.order_by('name'))

    def test_index_view_sort_by_percentage_desc(self):
        request = self.factory.get(reverse('index') + '?sort_by=percentage_desc')
        request.user = self.user
        response = index_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'insurance/insurance_types.html')
        self.assertQuerysetEqual(response.context_data['types'], InsuranceType.objects.order_by('-percentage'))


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.news = News.objects.create(title='Test News', content='Test Content', publish_date='2022-01-01')

    @patch('your_app.random_joke.RandomJokeService.get_random_joke', return_value='Funny Joke')
    @patch('your_app.cat_fact.CatFactService.get_random_fact', return_value='Cat Fact')
    def test_home_view(self, mock_joke, mock_cat_fact):
        request = self.factory.get(reverse('home'))
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'insurance/home.html')
        self.assertEqual(response.context_data['news'], self.news)
        self.assertEqual(response.context_data['joke'], 'Funny Joke')
        self.assertEqual(response.context_data['cat_facts'], 'Cat Fact')


class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.superuser = User.objects.create_superuser(username='superuser', password='12345')
        self.group_user = Group.objects.create(name='User')
        self.group_employee = Group.objects.create(name='Employee')
        self.group_user.user_set.add(self.user)
        self.group_employee.user_set.add(self.superuser)
        self.branch = CompanyBranch.objects.create(name='Branch A')
        self.type = InsuranceType.objects.create(name='Type A', description='Description A', percentage=0.05)

    def test_register_view_get(self):
        request = self.factory.get(reverse('register'))
        request.user = User()
        response = register(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context_data['form'], RegistrationForm)
        self.assertTemplateUsed(response, 'registration/registration.html')

    @patch('django.contrib.auth.models.User.objects.create_user')
    @patch('django.contrib.auth.models.Group.objects.get')
    def test_register_view_post_valid(self, mock_group, mock_create_user):
        mock_group.return_value = self.group_user
        mock_create_user.return_value = self.user
        request = self.factory.post(reverse('register'), data={'username': 'testuser', 'password': '12345'})
        request.user = User()
        response = register(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, '/home')
        self.assertTrue(InsuranceClient.objects.filter(user=self.user).exists())

    @patch('django.contrib.auth.models.User.objects.create_user')
    @patch('django.contrib.auth.models.Group.objects.get')
    def test_register_view_post_invalid(self, mock_group, mock_create_user):
        mock_group.return_value = self.group_user
        mock_create_user.return_value = self.user
        request = self.factory.post(reverse('register'), data={'username': 'testuser', 'password': '12345'})
        request.user = User()
        response = register(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context_data['form'], RegistrationForm)
        self.assertTemplateUsed(response, 'registration/registration.html')

    def test_custom_login_view_get(self):
        request = self.factory.get(reverse('custom_login'))
        request.user = User()
        response = custom_login(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context_data['form'], LoginForm)
        self.assertTemplateUsed(response, 'registration/login.html')

    @patch('django.contrib.auth.authenticate', return_value=None)
    def test_custom_login_view_post_invalid(self, mock_authenticate):
        request = self.factory.post(reverse('custom_login'), data={'username': 'testuser', 'password': '12345'})
        request.user = User()
        response = custom_login(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context_data['form'], LoginForm)
        self.assertTemplateUsed(response, 'registration/login.html')

    @patch('django.contrib.auth.authenticate', return_value=User.objects.get(username='testuser'))
    @patch('django.contrib.auth.login')
    def test_custom_login_view_post_valid(self, mock_login, mock_authenticate):
        request = self.factory.post(reverse('custom_login'), data={'username': 'testuser', 'password': '12345'})
        request.user = User()
        response = custom_login(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, '/home')

    def test_logout_view(self):
        request = self.factory.get(reverse('logout_view'))
        request.user = self.user
        response = logout_view(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, '/home')

    @patch('your_app.views.get_total_sales', return_value=1000)
    @patch('your_app.views.get_sales_statistics', return_value={})
    @patch('your_app.views.get_clients_age_statistics', return_value={})
    @patch('your_app.views.get_most_popular_insurance_type', return_value='Type A')
    @patch('your_app.views.get_agent_statistics', return_value={})
    @patch('your_app.views.visualize_sales_per_agent', return_value='<div>Chart</div>')
    @patch('your_app.views.visualize_statistics_per_clients_group', return_value='<div>Chart</div>')
    def test_superuser_extra_view(self, mock_total_sales, mock_sales_statistics, mock_clients_age_statistics, mock_popular_insurance, mock_agent_statistics, mock_sales_chart, mock_client_age_chart):
        request = self.factory.get(reverse('superuser_extra_view'))
        request.user = self.superuser
        response = superuser_profile_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/superuser_statistics.html')

    def test_user_profile_view(self):
        request = self.factory.get(reverse('user_profile_view'))
        request.user = self.user
        response = user_profile_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile.html')

    def test_employee_profile_view(self):
        agent = InsuranceAgent.objects.create(user=self.superuser, name='John', surname='Doe', second_name='Smith', age=30, address='123 Main St', phone_number='555-1234', branch_name=self.branch, job_position='Agent')
        request = self.factory.get(reverse('employee_profile_view'))
        request.user = self.superuser
        response = employee_profile_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/employee_profile.html')

    def test_superuser_profile_view(self):
        request = self.factory.get(reverse('superuser_profile_view'))
        request.user = self.superuser
        response = superuser_profile_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/superuser_profile.html')


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.review1 = Review.objects.create(text='Review 1', author=self.user, rating=5)
        self.review2 = Review.objects.create(text='Review 2', author=self.user, rating=7)

    def test_index_view(self):
        request = self.factory.get(reverse('index'))
        request.user = self.user
        response = index_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'insurance/reviews.html')
        self.assertEqual(list(response.context_data['reviews']), [self.review2, self.review1])

    def test_index_view_no_reviews(self):
        Review.objects.all().delete()
        request = self.factory.get(reverse('index'))
        request.user = self.user
        response = index_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'insurance/reviews.html')
        self.assertQuerysetEqual(response.context_data['reviews'], [])


class CreateViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.form_data = {
            'text': 'Test review',
            'author': self.user.pk,
            'rating': 8
        }

    def test_create_view_get(self):
        request = self.factory.get(reverse('create'))
        request.user = self.user
        response = create(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context_data['form'], MakeReview)
        self.assertTemplateUsed(response, 'insurance/make_review.html')

    @patch('your_app.forms.MakeReviewForm.is_valid', return_value=True)
    @patch('your_app.forms.MakeReviewForm.save')
    def test_create_view_post_valid(self, mock_save, mock_is_valid):
        request = self.factory.post(reverse('create'), data=self.form_data)
        request.user = self.user
        response = create(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, '/home')
        mock_save.assert_called_once()

    @patch('your_app.forms.MakeReviewForm.is_valid', return_value=False)
    def test_create_view_post_invalid(self, mock_is_valid):
        request = self.factory.post(reverse('create'), data=self.form_data)
        request.user = self.user
        response = create(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context_data['form'], MakeReview)
        self.assertTemplateUsed(response, 'insurance/make_review.html')
