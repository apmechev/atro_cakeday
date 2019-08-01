from icalendar import Calendar, Event
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

