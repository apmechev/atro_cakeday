from datetime import timedelta
from icalendar import Calendar, Event, Alarm
import inflect
p = inflect.engine()


class PlanetaryBirthday(Event):
    def __init__(self, planet='Earth', birthday_number=1, person_name='Your'):
        super(PlanetaryBirthday, self).__init__()

        # Let's be smart about how to display the name
        if person_name.lower() == 'your':
            suffix = ''
        else:
            suffix = "'s"

        self.add('summary', '{}{} {} Birthday on {}'.format(
            person_name, suffix, p.ordinal(birthday_number), planet))
        self.add('location', planet)

class DefaultAlarm(Alarm):

    def __init__(self):
        super(DefaultAlarm, self).__init__()

        self.add('action', 'display')
        self.add('trigger', timedelta(days=-1))
        self.add('description', 'Reminder: Get Cake!')

