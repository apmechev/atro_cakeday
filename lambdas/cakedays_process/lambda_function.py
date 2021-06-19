import os
import datetime
import logging
import time
import json
import boto3

from astro_cakeday.planets import Planets
from astro_cakeday.populate_cal import populate_ical

s3 = boto3.resource('s3')
bakery_bucket = s3.Bucket(os.environ.get("BAKERY_BUCKET_NAME",
                                         "bakery.cakedays.space"))


def lambda_handler(event, context):
    print(event)
    day = event.get("birthday", 1)
    month = event.get("birthmonth", 1)
    year = event.get("birthyear", 2000)
    start_year = event.get("cal_start", 1900)
    cal_end = event.get("cal_end", 2200)
    name = event.get("name", "Your ")

    if cal_end > 2200:
        cal_end = 2200

    birthdate = f"{year}-{month}-{day}"
    cal_start = f'{start_year}-01-01'
    cal_end = f'{cal_end}-01-01'
    try:
        datetime.datetime(year=year, month=month, day=day)
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"message": "ERROR: the birthday year, month, or day entered could not be understood; {}".format(str(e))})
        }

    merc_stag = event.get("mercury_stagger", 10)

    ven_stag = event.get("venus_stag", 10)
    custom_staggers = {'Mercury': merc_stag,
                       'Venus': ven_stag}
    planet_period = event.get("year_type", "tropical")

    planets = Planets(birthdate, staggers=custom_staggers,
                      period=planet_period)
    icalfile = populate_ical(planets, person_name=name,  birthday=birthdate,
                             cal_start=cal_start, cal_end=cal_end)
    filename = '/tmp/{}.ics'.format(icalfile)
    print(filename)
    result = bakery_bucket.upload_file(f"baked/{filename}",
                                       filename.split("/tmp")[1].replace("/", ""))
    print(result)

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
