import base64
import hashlib

from astropy.time import Time
import astropy.units as u
from astro_cakeday.birthday import PlanetaryBirthday
from astro_cakeday.planets import Planets
from icalendar import Calendar, Event


def populate_ical(person_name="Alex", birthday="1989-06-21", birthday_number=3):
    birthday_event = Time(birthday)

    cal = Calendar()
    planets = Planets(birthday_event)
    
    for number in range(1,birthday_number+1):
        for name in planets.planets:
            planet_bday = PlanetaryBirthday(str(name), number)
            planet_bday.add('dtstart', (birthday_event + number*planets.periods[name]).datetime)
            planet_bday.add('dtend', (birthday_event + number*planets.periods[name] + 1 * u.d).datetime)
            
            cal.add_component(planet_bday)
    filename = base64.b64encode(
        "{}-{}-{}".format(person_name, birthday, birthday_number).encode('utf-8')
        ).decode('ascii')[:-1]
    f = open('astro_cakeday/uploads/{}.ics'.format(filename), 'wb')
    f.write(cal.to_ical())
    f.close()
    return f.name
     
