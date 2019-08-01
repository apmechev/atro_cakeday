from astropy.time import Time
from astro_cakeday.planets import Planets
from poliastro.plotting import OrbitPlotter3D, OrbitPlotter2D

def generate_3D_plot(time, output):
    """Create an html file with a plotly 3D plot of the solar system at a specific time"""

    t = Time(time)
    P = Planets(t)

    frame = OrbitPlotter3D(dark=True)
    for planet in P.planets:
        frame.plot(P.orbits[planet], label=planet)

    frame.show().write_html(output)


def generate_2D_plot(time, output):
    """Create an html file with a plotly 2D plot of the solar system at a specific time"""

    t = Time(time)
    P = Planets(t)

    frame = OrbitPlotter2D()
    for planet in P.planets:
        frame.plot(P.orbits[planet], label=planet)

    frame.show().write_html(output)
