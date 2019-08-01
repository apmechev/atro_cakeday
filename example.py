from planet_birthdays import birthday_event 
from datetime import datetime, timedelta
from icalendar import Calendar, Event 

birthday = datetime.strptime("1989-06-21","%Y-%m-%d")

cal = Calendar()
uranus_1 = birthday_event.PlanetaryBirthday("Uranus", 1)
uranus_1.add('dtstart', birthday + timedelta(planet_lenghts['Uranus']))
uranus_1.add('dtend', birthday + timedelta(planet_lenghts['Uranus']+1))
cal.add_component(uranus_1)
