class UserError(Exception):
    """Base class for all User servoce errors"""
    pass


class UserInvalidRoleChange(UserError):
    """Raised when there a try to change the role of a user that do not follow the rules"""
