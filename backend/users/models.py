from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = None
    groups = None
    user_permissions = None

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password(self.password)
        return super().save(*args, **kwargs)