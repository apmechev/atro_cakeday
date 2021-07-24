import os
import datetime
import json
import boto3
import base64
from urllib.parse import urlparse, parse_qs

from astro_cakeday.planets import Planets
from astro_cakeday.populate_cal import populate_ical

s3 = boto3.resource('s3')
bucket_name = os.environ.get("BAKERY_BUCKET_NAME",
                             "bakery.cakedays.space")
bakery_bucket = s3.Bucket(bucket_name)


def unencode_body(event):
    body = event
    if 'body' in event.keys():
        body = event.get('body')
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8")
    body = parse_qs(body)
    for key in body:
        if type(body[key]) == list:
            body[key] = body[key][0]
    print(f"JSONified Body: {body}")
    return body


def lambda_handler(event, context):
    print(event)
    data = event
    if 'body' in event.keys():
        data = unencode_body(event)

    day = int(data.get("birthday", 1))
    month = int(data.get("birthmonth", 1))
    year = int(data.get("birthyear", 2000))
    start_year = int(data.get("cal_start", 1900))
    cal_end = int(data.get("cal_end", 2200))
    name = data.get("name", "Your")

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

    merc_stag = int(data.get("mercury_stagger", 10))

    ven_stag = int(data.get("venus_stag", 10))
    custom_staggers = {'Mercury': merc_stag,
                       'Venus': ven_stag}
    planet_period = data.get("year_type", "tropical")

    planets = Planets(birthdate, staggers=custom_staggers,
                      period=planet_period)
    icalfile = populate_ical(planets, person_name=name,  birthday=birthdate,
                             cal_start=cal_start, cal_end=cal_end)
    filename = '/tmp/{}.ics'.format(icalfile)
    s3_key = "baked/"+filename.split("/tmp")[1].replace("/", "")
    print(filename)
    result = bakery_bucket.upload_file(filename,
                                       s3_key)
    print(result)

    return {
        'statusCode': 200,
        'body': json.dumps({"Success": True,
                            "cake": f"http://{bucket_name}.s3-website.eu-central-1.amazonaws.com/{s3_key}"})
    }
