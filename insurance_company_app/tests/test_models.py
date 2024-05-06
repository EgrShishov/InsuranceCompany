from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group

from ..models import CompanyBranch, InsuranceAgent, InsuranceClient, InsuranceContract, InsuranceObject, InsuranceType, Review


class InsuranceAgentTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.branch = CompanyBranch.objects.create(name='Branch 1')

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')

    def test_create_insurance_agent(self):
        agent = InsuranceAgent.objects.create(
            user=self.user,
            name='John',
            surname='Doe',
            second_name='Smith',
            age=25,
            address='123 Main St',
            phone_number='+375 (29) 123-45-67',
            branch_name=self.branch,
            job_position='Agent',
            photo=SimpleUploadedFile('test_photo.jpg', b'content', content_type='image/jpeg')
        )
        self.assertEqual(InsuranceAgent.objects.count(), 1)

    def test_invalid_age(self):
        with self.assertRaises(ValidationError):
            InsuranceAgent.objects.create(
                user=self.user,
                name='John',
                surname='Doe',
                second_name='Smith',
                age=17,  # Invalid age
                address='123 Main St',
                phone_number='+375 (29) 123-45-67',
                branch_name=self.branch,
                job_position='Agent',
                photo=SimpleUploadedFile('test_photo.jpg', b'content', content_type='image/jpeg')
            )

    def test_invalid_phone_number(self):
        with self.assertRaises(ValidationError):
            InsuranceAgent.objects.create(
                user=self.user,
                name='John',
                surname='Doe',
                second_name='Smith',
                age=25,
                address='123 Main St',
                phone_number='invalid_phone_number',
                branch_name=self.branch,
                job_position='Agent',
                photo=SimpleUploadedFile('test_photo.jpg', b'content', content_type='image/jpeg')
            )

    def test_add_to_group_signal(self):
        agent = InsuranceAgent.objects.create(
            user=self.user,
            name='John',
            surname='Doe',
            second_name='Smith',
            age=25,
            address='123 Main St',
            phone_number='+375 (29) 123-45-67',
            branch_name=self.branch,
            job_position='Agent',
            photo=SimpleUploadedFile('test_photo.jpg', b'content', content_type='image/jpeg')
        )
        self.assertTrue(self.user.groups.filter(name='Employee').exists())


class InsuranceClientTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_group = Group.objects.create(name='User')

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')

    def test_create_insurance_client(self):
        client = InsuranceClient.objects.create(
            user=self.user,
            name='Jane',
            surname='Doe',
            second_name='Smith',
            age=25,
            address='123 Main St',
            phone_number='+375 (29) 123-45-67'
        )
        self.assertEqual(InsuranceClient.objects.count(), 1)

    def test_str_representation(self):
        client = InsuranceClient.objects.create(
            user=self.user,
            name='Jane',
            surname='Doe',
            second_name='Smith',
            age=25,
            address='123 Main St',
            phone_number='+375 (29) 123-45-67'
        )
        self.assertEqual(str(client), 'Jane')

    def test_invalid_age(self):
        with self.assertRaises(ValidationError):
            InsuranceClient.objects.create(
                user=self.user,
                name='Jane',
                surname='Doe',
                second_name='Smith',
                age=17,  # Invalid age
                address='123 Main St',
                phone_number='+375 (29) 123-45-67'
            )

    def test_invalid_phone_number(self):
        with self.assertRaises(ValidationError):
            InsuranceClient.objects.create(
                user=self.user,
                name='Jane',
                surname='Doe',
                second_name='Smith',
                age=25,
                address='123 Main St',
                phone_number='invalid_phone_number'
            )

    def test_add_to_user_group_signal(self):
        client = InsuranceClient.objects.create(
            user=self.user,
            name='Jane',
            surname='Doe',
            second_name='Smith',
            age=25,
            address='123 Main St',
            phone_number='+375 (29) 123-45-67'
        )
        self.assertTrue(self.user.groups.filter(name='User').exists())

    def test_valid_address_length(self):
        client = InsuranceClient.objects.create(
            user=self.user,
            name='Jane',
            surname='Doe',
            second_name='Smith',
            age=25,
            address='A' * 1000,
            phone_number='+375 (29) 123-45-67'
        )
        self.assertEqual(client.address, 'A' * 1000)

    def test_invalid_address_length(self):
        with self.assertRaises(ValidationError):
            InsuranceClient.objects.create(
                user=self.user,
                name='Jane',
                surname='Doe',
                second_name='Smith',
                age=25,
                address='A' * 1001,
                phone_number='+375 (29) 123-45-67'
            )

    def test_age_boundary_values(self):
        client_min_age = InsuranceClient(
            user=self.user,
            name='Jane',
            surname='Doe',
            second_name='Smith',
            age=18,
            address='123 Main St',
            phone_number='+375 (29) 123-45-67'
        )
        client_min_age.full_clean()

        client_max_age = InsuranceClient(
            user=self.user,
            name='Jane',
            surname='Doe',
            second_name='Smith',
            age=120,
            address='123 Main St',
            phone_number='+375 (29) 123-45-67'
        )
        client_max_age.full_clean()

    def test_create_multiple_clients_for_same_user(self):
        InsuranceClient.objects.create(
            user=self.user,
            name='Client 1',
            surname='Doe',
            second_name='Smith',
            age=25,
            address='123 Main St',
            phone_number='+375 (29) 123-45-67'
        )
        with self.assertRaises(ValidationError):
            InsuranceClient.objects.create(
                user=self.user,
                name='Client 2',
                surname='Doe',
                second_name='Smith',
                age=30,
                address='456 Elm St',
                phone_number='+375 (29) 987-65-43'
            )

    def test_invalid_user_group(self):
        invalid_group = Group.objects.create(name='Invalid Group')
        client = InsuranceClient.objects.create(
            user=self.user,
            name='Jane',
            surname='Doe',
            second_name='Smith',
            age=25,
            address='123 Main St',
            phone_number='+375 (29) 123-45-67'
        )
        self.assertFalse(self.user.groups.filter(name='Invalid Group').exists())

    def test_blank_name(self):
        with self.assertRaises(ValidationError):
            InsuranceClient.objects.create(
                user=self.user,
                name='',
                surname='Doe',
                second_name='Smith',
                age=25,
                address='123 Main St',
                phone_number='+375 (29) 123-45-67'
            )

    def test_blank_surname(self):
        with self.assertRaises(ValidationError):
            InsuranceClient.objects.create(
                user=self.user,
                name='Jane',
                surname='',
                second_name='Smith',
                age=25,
                address='123 Main St',
                phone_number='+375 (29) 123-45-67'
            )

    def test_blank_second_name(self):
        with self.assertRaises(ValidationError):
            InsuranceClient.objects.create(
                user=self.user,
                name='Jane',
                surname='Doe',
                second_name='',
                age=25,
                address='123 Main St',
                phone_number='+375 (29) 123-45-67'
            )

    def test_blank_address(self):
        with self.assertRaises(ValidationError):
            InsuranceClient.objects.create(
                user=self.user,
                name='Jane',
                surname='Doe',
                second_name='Smith',
                age=25,
                address='',
                phone_number='+375 (29) 123-45-67'
            )

    def test_blank_phone_number(self):
        with self.assertRaises(ValidationError):
            InsuranceClient.objects.create(
                user=self.user,
                name='Jane',
                surname='Doe',
                second_name='Smith',
                age=25,
                address='123 Main St',
                phone_number=''
            )


class InsuranceContractTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.insurance_type = InsuranceType.objects.create(name='Type A', percentage=0.1)
        cls.branch = CompanyBranch.objects.create(name='Branch 1')
        cls.agent = InsuranceAgent.objects.create(
            user=None,
            name='Agent',
            surname='Smith',
            second_name='John',
            age=30,
            address='123 Main St',
            phone_number='+375 (29) 123-45-67',
            branch_name=cls.branch,
            job_position='Agent',
            photo=None
        )
        cls.client = InsuranceClient.objects.create(
            user=None,
            name='Client',
            surname='Doe',
            second_name='Jane',
            age=25,
            address='456 Elm St',
            phone_number='+375 (29) 987-65-43'
        )

    def test_create_insurance_contract(self):
        contract = InsuranceContract.objects.create(
            date=timezone.now().date(),
            insurance_sum=1000.0,
            insurance_type=self.insurance_type,
            tariff_rate=0.05,
            branch_name=self.branch,
            insurance_object=None,
            agent=self.agent,
            client=self.client
        )
        self.assertEqual(InsuranceContract.objects.count(), 1)

    def test_str_representation(self):
        contract = InsuranceContract.objects.create(
            date=timezone.now().date(),
            insurance_sum=1000.0,
            insurance_type=self.insurance_type,
            tariff_rate=0.05,
            branch_name=self.branch,
            insurance_object=None,
            agent=self.agent,
            client=self.client
        )
        self.assertEqual(str(contract), 'Contract between Smith - Doe')

    def test_commission_calculation(self):
        contract = InsuranceContract.objects.create(
            date=timezone.now().date(),
            insurance_sum=1000.0,
            insurance_type=self.insurance_type,
            tariff_rate=0.05,
            branch_name=self.branch,
            insurance_object=None,
            agent=self.agent,
            client=self.client
        )
        self.assertEqual(contract.commission, 1000.0 * 0.05)

    def test_agent_salary_calculation(self):
        contract = InsuranceContract.objects.create(
            date=timezone.now().date(),
            insurance_sum=1000.0,
            insurance_type=self.insurance_type,
            tariff_rate=0.05,
            branch_name=self.branch,
            insurance_object=None,
            agent=self.agent,
            client=self.client
        )
        self.assertEqual(contract.agent_salary, (1000.0 * 0.05) * 0.1)

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            InsuranceContract.objects.create(
                date='invalid_date',  # Invalid date format
                insurance_sum=1000.0,
                insurance_type=self.insurance_type,
                tariff_rate=0.05,
                branch_name=self.branch,
                insurance_object=None,
                agent=self.agent,
                client=self.client
            )


class InsuranceObjectTestCase(TestCase):

    def test_create_insurance_object(self):
        insurance_object = InsuranceObject.objects.create(
            name='Car',
            description='Insurance for cars'
        )
        self.assertEqual(InsuranceObject.objects.count(), 1)

    def test_str_representation(self):
        insurance_object = InsuranceObject.objects.create(
            name='Car',
            description='Insurance for cars'
        )
        self.assertEqual(str(insurance_object), 'Car')

    def test_blank_name(self):
        with self.assertRaises(ValueError):
            InsuranceObject.objects.create(
                name='',  # Blank name
                description='Insurance for cars'
            )

    def test_blank_description(self):
        insurance_object = InsuranceObject.objects.create(
            name='Car',
            description=''
        )
        self.assertEqual(insurance_object.description, '')

    def test_max_length_name(self):
        insurance_object = InsuranceObject.objects.create(
            name='A' * 100,
            description='Insurance for cars'
        )
        self.assertEqual(insurance_object.name, 'A' * 100)

    def test_invalid_max_length_name(self):
        with self.assertRaises(ValueError):
            InsuranceObject.objects.create(
                name='A' * 101,
                description='Insurance for cars'
            )


class InsuranceTypeTestCase(TestCase):

    def test_create_insurance_type(self):
        insurance_type = InsuranceType.objects.create(
            name='Car Insurance',
            description='Insurance for cars',
            percentage=0.05
        )
        self.assertEqual(InsuranceType.objects.count(), 1)

    def test_str_representation(self):
        insurance_type = InsuranceType.objects.create(
            name='Car Insurance',
            description='Insurance for cars',
            percentage=0.05
        )
        self.assertEqual(str(insurance_type), 'Car Insurance')

    def test_blank_name(self):
        with self.assertRaises(ValueError):
            InsuranceType.objects.create(
                name='',
                description='Insurance for cars',
                percentage=0.05
            )

    def test_blank_description(self):
        insurance_type = InsuranceType.objects.create(
            name='Car Insurance',
            description='',
            percentage=0.05
        )
        self.assertEqual(insurance_type.description, '')

    def test_invalid_percentage(self):
        with self.assertRaises(ValueError):
            InsuranceType.objects.create(
                name='Car Insurance',
                description='Insurance for cars',
                percentage=-0.05
            )

    def test_percentage_exceeds_one(self):
        with self.assertRaises(ValueError):
            InsuranceType.objects.create(
                name='Car Insurance',
                description='Insurance for cars',
                percentage=1.5
            )

    def test_max_length_name(self):
        insurance_type = InsuranceType.objects.create(
            name='A' * 100,
            description='Insurance for cars',
            percentage=0.05
        )
        self.assertEqual(insurance_type.name, 'A' * 100)

    def test_invalid_max_length_name(self):
        with self.assertRaises(ValueError):
            InsuranceType.objects.create(
                name='A' * 101,
                description='Insurance for cars',
                percentage=0.05
            )


class ReviewModelTestCase(TestCase):
    def setUp(self):
        self.client = InsuranceClient.objects.create(
            name='John',
            surname='Doe',
            second_name='Smith',
            age=30,
            address='123 Main St',
            phone_number='555-1234'
        )

    def test_review_creation(self):
        review = Review.objects.create(
            text="This is a test review",
            author=self.client,
            rating=5
        )
        self.assertEqual(review.text, "This is a test review")
        self.assertEqual(review.author, self.client)
        self.assertEqual(review.rating, 5)
        self.assertIsInstance(review.created_at, datetime)

    def test_review_str_representation(self):
        review = Review.objects.create(
            text="Another test review",
            author=self.client,
            rating=8
        )
        self.assertEqual(str(review), "Review by Doe - Rating: 8")

    def test_review_clean_method(self):

        review = Review(
            text="Valid review",
            author=self.client,
            rating=7
        )
        review.full_clean()

        review.rating = 0
        with self.assertRaises(ValidationError):
            review.full_clean()

        review.rating = 11
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_review_ordering(self):
        review1 = Review.objects.create(
            text="Review 1",
            author=self.client,
            rating=6
        )
        review2 = Review.objects.create(
            text="Review 2",
            author=self.client,
            rating=9
        )
        review3 = Review.objects.create(
            text="Review 3",
            author=self.client,
            rating=3
        )

        reviews = Review.objects.all()
        self.assertEqual(reviews[0], review3)
        self.assertEqual(reviews[1], review2)
        self.assertEqual(reviews[2], review1)