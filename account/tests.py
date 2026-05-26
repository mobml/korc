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

    def test_superuser_create(self):
        user = services.superuser_create(email="test@email.com", password="testpass")
        user_two = services.superuser_create(email="test1@email.com", password="testpass")
        user_three = services.superuser_create(email="test2@email.com", password="testpass")

        total = User.objects.count()
            
        self.assertEqual(user.role, User.Role.OWNER)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user_two.email, user.email)
        self.assertEqual(user_three.email, user.email)
        self.assertEqual(1, total)

    def test_users_list_all(self):
        services.user_create(email="test@email.com", password="pass")
        services.user_create(email="test1@email.com", password="pass")
        services.user_create(email="test2@email.com", password="pass")

        users_list = services.users_list_all()

        self.assertEqual(len(users_list), 3)
        self.assertEqual(users_list[0].email, "test@email.com")
        self.assertEqual(users_list[1].email, "test1@email.com")
        self.assertEqual(users_list[2].email, "test2@email.com")
