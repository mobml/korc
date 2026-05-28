import uuid
from account.exceptions import UserInvalidRoleChange, SuperUserDeactivationError, SuperUserExists
import email
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
        
        with self.assertRaisesMessage(SuperUserExists, "The owner user already exists"):
            user_two = services.superuser_create(email="test1@email.com", password="testpass")

        total = User.objects.count()
            
        self.assertEqual(user.role, User.Role.OWNER)
        self.assertTrue(user.is_superuser)
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

    def test_users_list_active(self):
        user_one = services.user_create(email="test@email.com", password="pass")
        user_two = services.user_create(email="test1@email.com", password="pass")
        services.user_create(email="test2@email.com", password="pass")

        active_users = services.users_list_active()

        self.assertEqual(len(active_users), 3)

        user_one = services.user_toggle_active(user_one)
        user_two = services.user_toggle_active(user_two)

        active_users = services.users_list_active()

        self.assertEqual(len(active_users), 1)
        
        services.user_toggle_active(user_one)
        services.user_toggle_active(user_two)

        active_users = services.users_list_active()
        self.assertEqual(len(active_users), 3)

    def test_superuser_change_role(self):
        user = services.superuser_create(email="test@email.com", password="pass")

        with self.assertRaisesMessage(UserInvalidRoleChange, "The user owner role cannot change"):
            services.user_change_role(user, User.Role.ADMIN)            

    def test_user_does_not_exists_change_role(self):
        id = uuid.uuid4()
        user = User(id=id)
        with self.assertRaisesMessage(User.DoesNotExist, "There is no such user"):
            services.user_change_role(user, User.Role.ADMIN)            

    def test_user_change_role(self):
        user = services.user_create(email="test@email.com", password="pass")

        user = services.user_change_role(user, User.Role.ADMIN)
        self.assertEqual(User.Role.ADMIN, user.role)

    def test_user_toggle_active_owner(self):
        user = services.superuser_create(email="test@email.com", password="pass")

        with self.assertRaisesMessage(SuperUserDeactivationError, "The user owner is always active"):
            services.user_toggle_active(user)

    def test_user_toggle_active_no_existent_user(self):
        id = uuid.uuid4()
        user = User(id=id)
        with self.assertRaisesMessage(User.DoesNotExist, "There is no such user"):
            services.user_toggle_active(user)            

    def test_user_toggle_active(self):
        user = services.user_create(email="test@email.com", password="pass")

        user = services.user_toggle_active(user)

        self.assertEqual(user.is_active, False)
