import base64

from astropy.time import Time
from astro_cakeday.birthday import PlanetaryBirthday
from astro_cakeday.planets import Planets, PLANET_DB
from icalendar import Calendar

# TODO: I want birthdays from when I was 12 - 13, e.g.

def populate_ical(person_name="Alex", birthday="1989-06-21", birthday_number=3):
    birthday_event = Time(birthday)

    cal = Calendar()
    planets = Planets(birthday_event)
    
    for number in range(1,birthday_number+1):
        for name in planets.planets:
            planet_bday = PlanetaryBirthday(str(name), number * PLANET_DB[name])
            new_birthday_date = planets.get_birthday(name, number)
            new_birthday_date.out_subfmt = 'date'
            planet_bday.add('dtstart', new_birthday_date.datetime.date())

            cal.add_component(planet_bday)
    filename = base64.b64encode(
        "{}-{}-{}".format(person_name, birthday, birthday_number).encode('utf-8')
        ).decode('ascii')[:-1]
    f = open('astro_cakeday/uploads/{}.ics'.format(filename), 'wb')
    f.write(cal.to_ical())
    f.close()
    result_file = "http://cakedays.space/uploads/{}.ics".format(filename)
    return result_file
     
