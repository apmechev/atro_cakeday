import astropy.units as u
from astropy.time import Time


class Planets():

    def __init__(self, epoch, staggers={}):

        if type(epoch) is not Time:
            self.epoch = Time(epoch)
        else:
            self.epoch = epoch

        self.periods = {'Mercury': 87.97 * u.d,
                        'Venus': 224.70 * u.d,
                        'Earth': 365.36 * u.d,
                        'Mars': 686.98 * u.d,
                        'Jupiter': 4332.82 * u.d,
                        'Saturn': 10755.70 * u.d,
                        'Uranus': 30687.15 * u.d,
                        'Neptune': 60190.03 * u.d}
        self.staggers = {'Mercury': 5,
                         'Venus': 2,
                         'Earth': 1,
                         'Mars': 1,
                         'Saturn': 1,
                         'Jupiter': 1,
                         'Neptune': 1,
                         'Uranus': 1}
        self.staggers.update(staggers)
        self.planets = list(self.periods.keys())

    def get_birthday(self, planet, birthday_number=1):

        # birthday will be an astropy.time.Time object
        birthday = self.epoch + self.periods[planet] * birthday_number * self.staggers[planet]
        birthday.out_subfmt = 'date'

        return birthday

