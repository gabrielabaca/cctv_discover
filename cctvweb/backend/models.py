from django.db import models
import uuid

class Devices(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    
    model_uuid = models.ForeignKey(
        "DevicesModels",
        on_delete=models.RESTRICT,
        blank=True,
        null=True
    )

    ip = models.GenericIPAddressField(protocol='both', unique=True, db_index=True)
    port = models.CharField(max_length=10)
    full_address = models.CharField(null=True, blank=True, max_length=255)

    # SNAPS
    screen_shot = models.ImageField(upload_to='screen_shots/', null=True, blank=True)
    last_screen_shot_at = models.BigIntegerField(null=True, blank=True)

    # GEO
    latitude = models.FloatField(db_index=True, null=True, blank=True)
    longitude = models.FloatField(db_index=True, null=True, blank=True)
    country = models.CharField(max_length=85, null=True, blank=True)
    city = models.CharField(max_length=84, null=True, blank=True)

    # Status
    is_online = models.BooleanField(default=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    status = models.BooleanField(default=True, db_index=True)

    # Fetch Method
    fetch_method = models.CharField(default='Shodan', max_length=100)

    # Created and modify data
    created_at = models.BigIntegerField()
    updated_at = models.BigIntegerField(null=True, blank=True)

    # Extra data like as web version, plugin, eTag
    extra_data = models.JSONField(null=True, blank=True)

    # Search Params
    query_search = models.CharField(max_length=250, null=True, blank=True)

class DevicesModels(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    name = models.CharField(max_length=64)
    