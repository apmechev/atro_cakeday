import astropy.units as u
from astropy.time import Time
from poliastro.twobody import Orbit
from poliastro.bodies import Mercury, Venus, Earth, Mars, Saturn, Jupiter, Neptune, Uranus, Pluto


class Planets():

    def __init__(self, epoch):

        if type(epoch) is not Time:
            epoch = Time(epoch)

        self.orbits = {}
        self.periods = {}
        for name, body in zip(['Mercury', 'Venus', 'Earth', 'Mars', 'Saturn', 'Jupiter', 'Neptune', 'Uranus'],
                              [Mercury, Venus, Earth, Mars, Saturn, Jupiter, Neptune, Uranus]):
            orbit = Orbit.from_body_ephem(body, epoch)
            self.orbits[name] = orbit
            self.periods[name] = orbit.period.to(u.d)

