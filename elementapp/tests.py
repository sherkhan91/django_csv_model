from django.test import TestCase
from .models import information
import validators
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.encoding import force_text

# Create your tests here.

""" this test is checking model """

class informationModelTest(TestCase):
    """test names are self describing itself so not adding up further comments on each function """

    @classmethod
    def setUpTestData(TestCase):
        # setting up an object to be used by all
        information.objects.create(title='test',description='this description',image='http://www.test.com')

    def test_title_label(self):
        mTitle =  information.objects.get(id=1)
        field_label = information._meta.get_field('title').verbose_name
        self.assertEqual(field_label,'title')
    
    def test_image_max_length(self):
        info =  information.objects.get(id=1)
        max_length = info._meta.get_field('image').max_length
        self.assertEqual(max_length,500)
    
    def test_image_url(self):
        test_url = information.objects.get(id=1).image
        self.assertEqual(validators.url(test_url),True)


""" this test create a user and login, we can only use functionality from admin panel by default! """
class SigninTest(TestCase):

    @classmethod
    def setUp(self):
        """ setting up a test user  """
        self.user = User.objects.create_user('shertest','sher@test.com','Qwerty123?')
        self.user.save()
        

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='shertest', password='Qwerty123?')
        self.assertTrue((user is not None ) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong_sher_name', password='Qwerty123?')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='shertest', password='sher_wrong_password')
        self.assertFalse(user is not None and user.is_authenticated)


"""checking the loading of default index page"""
""" assume running on following, python manage.py runserver 0.0.0.0:80 """
class ViewTestCase(TestCase):

    @classmethod
    def setUpTestData(TestCase):
        # setting up an object to be used by all
        info  =information.objects.create(title='test',description='this description',image='http://www.test.com')
        info.save()

    def test_index_loads_properly(self):
        response =self.client.get('http://www.0.0.0.0:80/elementapp/')
        self.assertEqual(response.status_code,200)
    
    """checking if entered informations gets back """
    def test_json_response(self):
        response = self.client.get('http://www.0.0.0.0:80/elementapp/getinformation')
        self.assertEqual(response.status_code,200)
        




