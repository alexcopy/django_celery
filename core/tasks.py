import csv
import os
from celery import shared_task
from django.core.files.temp import NamedTemporaryFile
from .models import Download, ImmunizationLegalEntries
import requests

@shared_task
def write_file_toDb(fpath):
    ImmunizationLegalEntries.objects.all().delete()
    with open(fpath) as csvfile:
        reader = csv.DictReader(csvfile)
    for row in reader:
        new_immunization = ImmunizationLegalEntries(
            legal_entity_id=row['legal_entity_id'],
            legal_entity_name=row['legal_entity_name'],
            legal_entity_edrpou=row['legal_entity_edrpou'],
            care_type=row['care_type'],
            property_type=row['property_type'],
            legal_entity_email=row['legal_entity_email'],
            legal_entity_phone=row['legal_entity_phone'],
            legal_entity_owner_name=row['legal_entity_owner_name'],
            registration_area=row['registration_area'],
            registration_settlement=row['registration_settlement'],
            registration_addresses=row['registration_addresses'],
            lat=row['lat'],
            lng=row['lng'],
        )
        new_immunization.save()
    os.remove(fpath)


def load_file(url, tmp, etag):
    headers = {'If-None-Match': etag}
    with requests.request("GET", url, headers=headers, stream=True) as res:
        print(res.headers)
        if res.status_code == requests.codes.ok:
            for chunk in res.iter_content(chunk_size=8192):
                tmp.write(chunk)
            etag = res.headers.get('ETag')
        else:
            print(f'{url}: {res.reason} {res.status_code}')
    return etag


@shared_task
def get_data_task():
  for f in Download.objects.all():
    try:
        tmp = NamedTemporaryFile(delete=False)
        url = f.url
        new_etag = load_file(url, tmp, f.etag)
        filesize = os.path.getsize(tmp.name)
        if filesize > 10 and not f.etag == new_etag:
            write_file_toDb.delay(tmp.name)
            f.etag=new_etag
            f.save()
        tmp.close()
    finally:
        print('Error')
