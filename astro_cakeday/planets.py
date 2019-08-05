import astropy.units as u
from astropy.time import Time


class Planets():

    def __init__(self, epoch, staggers={}, period='tropical'):

        if type(epoch) is not Time:
            self.epoch = Time(epoch)
        else:
            self.epoch = epoch
        self.period_kind = period
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

        self.sidereal_periods ={'Mercury': 87.969 * u.d,
                        'Venus': 224.701 * u.d,
                        'Earth': 365.256 * u.d,
                        'Mars': 686.980 * u.d,
                        'Jupiter': 4332.589 * u.d,
                        'Saturn': 10759.22 * u.d,
                        'Uranus': 30685.400 * u.d,
                        'Neptune': 60189.00 * u.d}

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

        
    @property
    def periods(self):
        if self.period_kind == 'tropical':
            return self.tropical_periods
        else:
            return self.sidereal_periods

    def get_birthday(self, planet, birthday_number=1):

        # birthday will be an astropy.time.Time object
        birthday = self.epoch + self.periods[planet] * birthday_number * self.staggers[planet]
        birthday.out_subfmt = 'date'

        return birthday

