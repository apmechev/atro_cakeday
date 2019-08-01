import astropy.units as u
from astropy.time import Time
from poliastro.twobody import Orbit
from poliastro import bodies

PLANETS_TO_USE = ['Mercury', 'Venus', 'Earth', 'Mars', 'Saturn', 'Jupiter', 'Neptune', 'Uranus']

PLANET_DB = {'Mercury': 15,
             'Venus': 5,
             'Earth': 1,
             'Mars': 1,
             'Saturn': 1,
             'Jupiter': 1,
             'Neptune': 1,
             'Uranus': 1}

class Planets():

    def __init__(self, epoch):

        if type(epoch) is not Time:
            self.epoch = Time(epoch)
        else:
            self.epoch = epoch

        self.orbits = {}
        self.periods = {}
        self.planets = PLANETS_TO_USE

        for planet in PLANETS_TO_USE:

            try:
                body = getattr(bodies, planet)
            except AttributeError:
                raise AttributeError('Currently do not have data for {}'.format(planet))

            orbit = Orbit.from_body_ephem(body, self.epoch)
            self.orbits[planet] = orbit
            self.periods[planet] = orbit.period.to(u.d)

    def get_birthday(self, planet, birthday_number=1):

        birthday = self.epoch + self.periods[planet] * birthday_number * PLANET_DB[planet]

        return birthday

