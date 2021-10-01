from django.db import models


class Download(models.Model):
    hash = models.CharField(max_length=255)
    url = models.URLField()
    tmp = models.FileField()
    etag = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class ImmunizationLegalEntries(models.Model):
    legal_entity_id = models.CharField(max_length=255)
    legal_entity_name = models.CharField(max_length=255)
    legal_entity_edrpou = models.CharField(max_length=255)
    care_type = models.CharField(max_length=255)
    property_type = models.CharField(max_length=255)
    legal_entity_email = models.CharField(max_length=255)
    legal_entity_phone = models.CharField(max_length=255)
    legal_entity_owner_name = models.CharField(max_length=255)
    registration_area = models.CharField(max_length=255)
    registration_settlement = models.CharField(max_length=255)
    registration_addresses = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    lng = models.CharField(max_length=255)
