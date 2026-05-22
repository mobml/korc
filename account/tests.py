from django.test import TestCase
from account import services
from account.models import User


class UserServiceCreateTest(TestCase):
    def test_user_create(self):
        services.user_create(email="test@email.com", password="testpassword")
        services.user_create(email="test1@email.com", password="testpassword")

        user_one = User.objects.get(email="test@email.com")
        user_two = User.objects.get(email="test1@email.com")

        total = User.objects.count()

        self.assertEqual(user_one.role, User.Role.CASHIER)
        self.assertEqual(user_two.role, User.Role.CASHIER)
        self.assertEqual(2, total)
