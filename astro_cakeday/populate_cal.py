import base64

from astropy.time import Time
from astro_cakeday.birthday import PlanetaryBirthday, DefaultAlarm
from astro_cakeday.planets import Planets, PLANET_DB
from icalendar import Calendar

# TODO: I want birthdays from when I was 12 - 13, e.g.

HARDSTOP = Time('2300-01-01')
SAMLINK = "<a href=https://samreay.github.io/SpaceBirthdays/?date={}-{}-{}>Link to app</a>"

def populate_ical(person_name="Alex", birthday="1989-06-21",
                  birthday_number=3, PLANET_DB=PLANET_DB, cal_start=None, cal_end='2100-01-01'):
    birthday_time = Time(birthday)

    if cal_start is None:
        cal_start = birthday
    cal_start = Time(cal_start)

    cal_end = Time(cal_end)
    if cal_end > HARDSTOP:
        cal_end = HARDSTOP

    cal = Calendar()

    # Let's be smart about how to display the name
    if person_name.lower() == 'your':
        suffix = ''
    else:
        suffix = "'s"

    # It's not clear from ical docs which of these is correct. Let's use both!
    cal.add('X-WR-CALNAME', '{}{} planetary cake days'.format(person_name, suffix))
    cal.add('NAME', '{}{} planetary cake days'.format(person_name, suffix))

    planets = Planets(birthday_time)
    sam_link = SAMLINK.format(birthday_time.datetime.year,
                              birthday_time.datetime.month,
                              birthday_time.datetime.day)

    for name in planets.planets:
        start_number = (cal_start - birthday_time) / planets.periods[name] / PLANET_DB[name]
        number = int(start_number)
        new_birthday_date = cal_start

        while new_birthday_date <= cal_end:
            planet_bday = PlanetaryBirthday(str(name), number * PLANET_DB[name], person_name=person_name)
            new_birthday_date = planets.get_birthday(name, number)

            if new_birthday_date > cal_end:
                break

            new_birthday_date.out_subfmt = 'date'
            planet_bday.add('dtstart', new_birthday_date.datetime.date())
            add_link_to_sam_magic(planet_bday, sam_link)

            cal.add_component(planet_bday)
            number += 1

    filename = base64.b64encode(
        "{}-{}-{}".format(person_name, birthday, birthday_number).encode('utf-8')
        ).decode('ascii')[:-1]
    f = open('astro_cakeday/uploads/{}.ics'.format(filename), 'wb')
    f.write(cal.to_ical())
    f.close()
    result_file = "http://cakedays.space/calendars/{}.ics".format(filename)
    return result_file

def add_link_to_sam_magic(event, link_str):

    event.add('X-ALT-DESC', link_str, parameters={'fmttype': 'text/html'})
