from icalendar import Calendar, Event
import inflect
p = inflect.engine()


class PlanetaryBirthday(Event):
    def __init__(self, planet='Earth', birthday_number=1):
        super(PlanetaryBirthday, self).__init__()
        self.add('summary', 'Your {} Birthday on {}'.format(
            p.ordinal(birthday_number), planet))

