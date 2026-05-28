from account.exceptions import UserInvalidRoleChange, SuperUserDeactivationError
from account.models import User
from django.db.models import F

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

def user_change_role(user: User, role: User.Role) -> User:
    if user.role == User.Role.OWNER:
        raise UserInvalidRoleChange("The user owner role cannot change")

    update_count = User.objects.filter(id=user.id).update(role=role)

    if update_count == 0:
        raise User.DoesNotExist("There is no such user")

    user.role = role
    return user

def user_toggle_active(user: User) -> User:
    if user.role == User.Role.OWNER:
        raise SuperUserDeactivationError("The user owner is always active")

    update_count = User.objects.filter(id=user.id).update(
        is_active=~F("is_active")
    )

    if update_count == 0:
        raise User.DoesNotExist("There is no such user")

    user.is_active = not user.is_active
    return user
