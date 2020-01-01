from django.test import TestCase,Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):
    def setUp(self):#keyword---this func approached before test functions
        self.client=Client()
        self.admin_user=get_user_model().objects.create_superuser(
        email='hegde.akash1999@gmail.com',
        password='pass123'
        )
        self.client.force_login(self.admin_user)
        self.user=get_user_model().objects.create_user(
        email='akkistud@gmail.com',
        password='pass567',
        name='abc'
        )
    def test_users_listed(self):
        """Test that users listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res,self.user.name)
        self.assertContains(res,self.user.email)

    def test_user_edit_page(self):
        """Test user edit page"""
        url=reverse("admin:core_user_change",args=[self.user.id])
        res=self.client.get(url)
        self.assertEqual(res.status_code,200)

    def test_wait_for_db_create_user_page(self):
        """Test that create user page works"""
        url=reverse('admin:core_user_add')
        res=self.client.get(url)
        self.assertEqual(res.status_code,200)
