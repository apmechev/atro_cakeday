import astropy.units as u
from astropy.time import Time
from poliastro.twobody import Orbit
from poliastro import bodies

PLANETS_TO_USE = ['Mercury', 'Venus', 'Earth', 'Mars', 'Saturn', 'Jupiter', 'Neptune', 'Uranus']

class Planets():

    def __init__(self, epoch):

        if type(epoch) is not Time:
            epoch = Time(epoch)

        self.orbits = {}
        self.periods = {}
        self.planets = PLANETS_TO_USE

        for planet in PLANETS_TO_USE:

            try:
                body = getattr(bodies, planet)
            except AttributeError:
                raise AttributeError('Currently do not have data for {}'.format(planet))

            orbit = Orbit.from_body_ephem(body, epoch)
            self.orbits[planet] = orbit
            self.periods[planet] = orbit.period.to(u.d)

