"""
Functions for access control.
"""
from django.contrib.auth import get_user_model


def authenticated(user):
    """For authenticated users."""
    return user.is_active and user.is_authenticated


def staff(user):
    """For employers and superusers."""
    return authenticated(user) and (user.is_staff or user.is_superuser)


def superuser(user):
    """For superusers only."""
    return authenticated(user) and user.is_superuser


User = get_user_model()
view_perm = '%s.view_%s' % (User._meta.app_label, User._meta.model_name)


def view_users(user):
    """For users with view permission for User model."""
    return authenticated(user) and user.has_perm(view_perm)
