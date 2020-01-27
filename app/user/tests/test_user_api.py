from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:Me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the users API(public)"""

    def setUp(self):
        self.client=APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload"""
        payload={
        'email':'hegde.akash1999@gmail.com',
        'password':'testpass',
        'name':'Akash Hegde',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)

    def test_case_user_exists(self):
        """Test creating an existing user fails"""
        payload={
            'email':'hegde.akash1999@gmail.com',
            'password':'testpass',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test password should be more than 5 characters"""
        payload={
            'email':'hegde.akash1999@gmail.com',
            'password':'pass1',
        }
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
        email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that token is created for user"""
        payload={'email':'hegde.akash@gmail.com', 'password':'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL,payload)
        #print("Response=")
        #print(res)
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that the token is not created if invalid credentials given"""
        create_user(email='hegde.akash1999@gmail.com',password='testpass')
        payload={'email': 'hegde.akash1999@gmail.com',
                 'password': 'something'}
        res =  self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token isnt created if no user exists"""
        payload={'email':'hegde.akash1999@gmail.com','password':'testpass'}
        res =  self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        payload={'email':'hegde.akash1999@gmail.com','password':''}
        res =  self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res=self.client.get(ME_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user=create_user(
        email='hegde.akash1999@gmail.com',
        password='testpass',
        name='Akash'
        )
        self.client=APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res=self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,
        {'name':self.user.name,
        'email':self.user.email
        })
    def test_post_me_not_allowed(self):
        """Test that POST is not allowed"""
        res=self.client.post(ME_URL,{})
        self.assertEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test update feature"""
        payload={'password':'newtestpass','name':'Akash Hegde'}
        res=self.client.patch(ME_URL,payload)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(self.user.name,payload['name'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
