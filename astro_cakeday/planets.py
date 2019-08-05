import astropy.units as u
from astropy.time import Time


class Planets():

    def __init__(self, epoch, staggers={}):

        if type(epoch) is not Time:
            self.epoch = Time(epoch)
        else:
            self.epoch = epoch
        # Taken from https://nssdc.gsfc.nasa.gov/planetary/factsheet/
        # We use the tropical Orbital period
        self.tropical_periods = {'Mercury': 87.968 * u.d,
                        'Venus': 224.695 * u.d,
                        'Earth': 365.242 * u.d,
                        'Mars': 686.973 * u.d,
                        'Jupiter': 4330.595 * u.d,
                        'Saturn': 10746.94 * u.d,
                        'Uranus': 30588.740 * u.d,
                        'Neptune': 59799.9 * u.d}
        @property
        def periods(self,kind='tropical'):
            if kind == 'tropical':
                return self.tropical_periods
            else:
                return self.sidereal_periods

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

