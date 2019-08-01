from birthday import PlanetaryBirthday 
from planets import planet_lengths
from datetime import datetime, timedelta
from icalendar import Calendar, Event 

birthday_event = datetime.strptime("1989-06-21","%Y-%m-%d")
birthday_number = 3

cal = Calendar()

for number in range(0,birthday_number):
    for name in planet_lengths:
        planet = PlanetaryBirthday(str(name), number)
        planet.add('dtstart', birthday_event + timedelta(planet_lengths[name]))
        planet.add('dtend', birthday_event + timedelta(planet_lengths[name]+1))
        
        cal.add_component(planet)
