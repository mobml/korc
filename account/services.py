from account.models import User


def user_create(email: str, password: str) -> User:
    user = User.objects.create_user(email=email, password=password)

    return user

def superuser_create(email: str, password: str) -> User:

    #if already existes an OWNER then we return None
    # Only can exits one owner

    try:
        user = User.objects.get(role=User.Role.OWNER)
    except User.DoesNotExist:
        user = User.objects.create_superuser(email=email, password=password)    
    
    return user

#this functions list all users
# even that are not active
def users_list_all() -> list[User]:
    users = User.objects.all()

    return users
