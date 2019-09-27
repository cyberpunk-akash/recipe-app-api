from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = 'hegde.akash1999@gmail.com'
        password = 'admin'
        user = get_user_model().objects.create_user(
            email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test if email for new user is normalized"""
        email = 'hegde.akash1999@GMAIL.COM'
        password = 'admin'
        user = get_user_model().objects.create_user(
            email=email, password=password)
        self.assertEqual(user.email, email.lower())

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'hegde.akash1999@gmail.com', 'superadmin'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_new_user_invalid_email(self):
        """Test creating user with no email creates error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')
