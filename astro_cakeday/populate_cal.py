from astro_cakeday.birthday import PlanetaryBirthday 
from astro_cakeday.planets import planet_lengths
from datetime import datetime, timedelta
from icalendar import Calendar, Event 


def populate_ical(birthday="1989-06-21", birthday_number=3):
    birthday_event = datetime.strptime(birthday,"%Y-%m-%d")

    cal = Calendar()

    for number in range(0,birthday_number+1):
        for name in planet_lengths:
            planet = PlanetaryBirthday(str(name), number)
            planet.add('dtstart', birthday_event + timedelta(planet_lengths[name]))
            planet.add('dtend', birthday_event + timedelta(planet_lengths[name]+1))
            
            cal.add_component(planet)
    
    print(cal)
