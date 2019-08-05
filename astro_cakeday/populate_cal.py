import base64
import os
import pkg_resources

from astropy.time import Time
from astro_cakeday.birthday import PlanetaryBirthday
from icalendar import Calendar
from datetime import datetime
import hashlib

if os.path.exists(pkg_resources.resource_filename('astro_cakeday', 'config.py')):
    from astro_cakeday.config import SECRET_KEY
else:
    SECRET_KEY = "NOSECRET"

# TODO: I want birthdays from when I was 12 - 13, e.g.

HARDSTOP = Time('2300-01-01')
SAMLINK = "<a href=https://samreay.github.io/SpaceBirthdays/?date={0}-{1:02d}-{2:02d}>Visualize it!</a>"

def populate_ical(planets, person_name="Alex", birthday="1989-06-21", cal_start='2018-01-01', cal_end='2100-01-01'):

    birthday_time = Time(birthday)

    try:
        cal_start_dt = datetime.strptime(cal_start,"%Y-%m-%d")
    except ValueError:
        cal_start_dt = datetime.strptime(birthday,"%Y-%m-%d")
        cal_start = birthday
    bday_dt = datetime.strptime(birthday,"%Y-%m-%d")
    if cal_start_dt.year < bday_dt.year:
        cal_start = birthday

    cal_start = Time(cal_start)

    try:
        cal_end = Time(cal_end)
    except ValueError:
        cal_end = HARDSTOP

    if cal_end > HARDSTOP:
        cal_end = HARDSTOP

    cal = Calendar()
    set_cal_name(cal, person_name)

    # We do this now because it will be the same inside every loop below
    sam_link = SAMLINK.format(birthday_time.datetime.year,
                              birthday_time.datetime.month,
                              birthday_time.datetime.day)

    for name in planets.planets:
        start_number = (cal_start - birthday_time) / planets.periods[name] / planets.staggers[name]
        number = int(start_number)
        new_birthday_date = cal_start

        while new_birthday_date <= cal_end:
            planet_bday = PlanetaryBirthday(str(name), number * planets.staggers[name], person_name=person_name)
            new_birthday_date = planets.get_birthday(name, number)

            if new_birthday_date > cal_end:
                break

            planet_bday.add('dtstart', new_birthday_date.datetime.date())
            add_link_to_sam_magic(planet_bday, sam_link)

            cal.add_component(planet_bday)
            number += 1

    filename = hashlib.sha256(
        "{}-{}-{}-{}".format(person_name, birthday, SECRET_KEY, planets).encode('ascii')
        ).hexdigest()
    with open('astro_cakeday/uploads/{}.ics'.format(filename), 'wb') as f:
        f.write(cal.to_ical())

    result_file = "http://cakedays.space/calendars/{}.ics".format(filename)
    return result_file


def set_cal_name(cal, person_name):

    # Let's be smart about how to display the name
    if person_name.lower() == 'your':
        suffix = ''
    else:
        suffix = "'s"
    # It's not clear from ical docs which of these is correct. Let's use both!
    cal.add('X-WR-CALNAME', '{}{} planetary cake days'.format(person_name, suffix))
    cal.add('NAME', '{}{} planetary cake days'.format(person_name, suffix))


def add_link_to_sam_magic(event, link_str):

    # It appears that some calendar apps support one of these and some the other. Let's have both
    event.add('X-ALT-DESC', link_str, parameters={'fmttype': 'text/html'})
    event.add('Description', link_str)
