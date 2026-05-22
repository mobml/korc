from account.models import User


def user_create(email: str, password: str):
    user = User.objects.create_user(email=email, password=password)

    return user
