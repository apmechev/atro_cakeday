from birthday import PlanetaryBirthday 
from planets import planet_lengths
from datetime import datetime, timedelta
from icalendar import Calendar, Event 

birthday_event = datetime.strptime("1989-06-21","%Y-%m-%d")

cal = Calendar()

for i in planet_lengths:
    print(i)

uranus_1 = PlanetaryBirthday("Uranus", 1)
uranus_1.add('dtstart', birthday_event + timedelta(planet_lengths['Uranus']))
uranus_1.add('dtend', birthday_event + timedelta(planet_lengths['Uranus']+1))

cal.add_component(uranus_1)
