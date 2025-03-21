from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from .managers import CustomUserManager


class User(AbstractUser, PermissionsMixin):
    """
    Custom User model that extends AbstractUser to include custom fields
    such as `type`, `gender`, and `profile_image`.
    """
    
    class Types(models.TextChoices):
        STAFF = "STAFF", "Staff"
        ENDUSER = "ENDUSER", "End User"

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )

    # Removed `username` field as it will be replaced by email
    username = None  

    # Added email as the unique identifier for authentication
    email = models.EmailField(
        _("email address"),
        unique=True,
        db_index=True
    )

    # Standard first and last name fields
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)

    # Gender selection with choices for male and female
    gender = models.CharField(
        _("Gender"), max_length=30, choices=GENDER_CHOICES, blank=True, null=True
    )

    # User type field, either STAFF or ENDUSER
    type = models.CharField(
        _("User Type"),
        max_length=50,
        choices=Types.choices,
        default=Types.STAFF,
    )

    # Profile image for users (used for both Staff and EndUser)
    profile_image = models.ImageField(
        upload_to='profile_images/', null=True, blank=True, help_text=_("Profile image of the user")
    )

    # A boolean to mark if the email is verified
    is_verified = models.BooleanField(
        default=False,
        help_text=_("Designates whether this user has verified their email.")
    )

    # Admin-level access flag for the user
    is_custom_admin = models.BooleanField(
        default=False,
        help_text=_("Designates whether this user has dashboard access to the site.")
    )

    # Automatically sets the date when the user is created
    date_joined = models.DateTimeField(default=timezone.now)

    # Replace username with email for login
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # Manager for custom user queries
    objects = CustomUserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class StaffManager(CustomUserManager):
    """
    Manager for filtering staff users from the custom User model.
    """
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.STAFF)


class EndUserManager(CustomUserManager):
    """
    Manager for filtering end-user users from the custom User model.
    """
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.ENDUSER)


class StaffUserProfile(models.Model):
    """
    Profile model specific to the staff user. It stores additional details 
    for staff users.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_profile")
    profile_image = models.ImageField(upload_to='staff_images/', blank=True, null=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Staff Profile"
        verbose_name_plural = "Staff Profiles"


class EndUserProfile(models.Model):
    """
    Profile model specific to the end-user. It stores additional details 
    for end users.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="end_user_profile")
    profile_image = models.ImageField(upload_to='end_user_images/', blank=True, null=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "End User Profile"
        verbose_name_plural = "End User Profiles"


# Signal handler to create or update profiles when a user is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    This ensures that each user has the correct profile model created or updated
    based on their user type.
    """
    if created:
        if instance.type == User.Types.STAFF:
            StaffUserProfile.objects.get_or_create(user=instance)
        elif instance.type == User.Types.ENDUSER:
            EndUserProfile.objects.get_or_create(user=instance)
    else:
        if instance.type == User.Types.STAFF:
            StaffUserProfile.objects.get_or_create(user=instance)
            EndUserProfile.objects.filter(user=instance).delete()
        elif instance.type == User.Types.ENDUSER:
            EndUserProfile.objects.get_or_create(user=instance)
            StaffUserProfile.objects.filter(user=instance).delete()
