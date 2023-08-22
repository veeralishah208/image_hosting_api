from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class ImageStorage(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        upload_to="user/image/%Y",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        blank=False,
        null=False,
        default=timezone.now
    )
    valid_till = models.DateTimeField(
        blank=False,
        null=False
    )

    def __str__(self):
        return self.user_id.username

    class Meta:
        db_table = "image_storage"
        verbose_name_plural = "Image Storage"


class Plan(models.Model):
    plan_name = models.CharField(
        max_length=150,
        blank=False,
        null=False
    )
    original_link = models.BooleanField(default=False)
    expiring_link = models.PositiveIntegerField(default=300)

    def __str__(self):
        return self.plan_name

class Thumbnail(models.Model):
    plan_id = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
    )
    thumbnail_sizes = models.IntegerField()

    def __str__(self):
        return self.plan_id.plan_name

class Subscription(models.Model):
    user_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )    
    plan_id = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.plan_id.plan_name