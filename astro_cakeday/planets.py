import astropy.units as u
from astropy.time import Time

PLANET_DB = {'Mercury': 5,
             'Venus': 2,
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

        self.planets = list(PLANET_DB.keys())
        self.periods = {'Mercury': 87.97 * u.d,
                        'Venus': 224.70 * u.d,
                        'Earth': 365.36 * u.d,
                        'Mars': 686.98 * u.d,
                        'Jupiter': 4332.82 * u.d,
                        'Saturn': 10755.70 * u.d,
                        'Uranus': 30687.15 * u.d,
                        'Neptune': 60190.03 * u.d}

    def get_birthday(self, planet, birthday_number=1):

        birthday = self.epoch + self.periods[planet] * birthday_number * PLANET_DB[planet]

        return birthday

