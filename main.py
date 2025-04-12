from astropy import units as u
from poliastro.bodies import Sun, Earth, Mars, Moon
from poliastro.twobody import Orbit
from poliastro.maneuver import Maneuver
from astropy.time import Time
# import math
# R_earth = 6378 #km
# R_mars = 3389 #km
# sun_mu = 1.327 * 10 ** 11 # km**3/s**2
# launch_date = Time("2027-01-15")
# arrival_date = Time("2027-10-01")
# earth_at_launch = Orbit.from_classical(
#     attractor = Sun,
#     a = 1.0 * u.au,
#     ecc = 0.0167 * u.one,
#     inc = 0 * u.deg,
#     raan = 0 * u.deg,
#     argp = 0 * u.deg,
#     nu = 300 * u.deg,
#     epoch = launch_date
# )
# r1 = earth_at_launch.r
# print(r1)

import math

vernal_equinox_date = Time("2026-03-21")
perihelion_earth = Time("2026-01-04")
print(f"time check {vernal_equinox_date - perihelion_earth}")
# Mars Parameters

mars_a = 1.523679 * u.AU  # Semi-major axis in AU
mars_e = 0.0934           # Eccentricity
mars_i = 1.85 * u.deg     # Inclination in degrees
mars_w = 286.5 * u.deg    # Argument of perihelion in degrees
mars_OM = 49.558 * u.deg  # Longitude of ascending node in degrees

# Mars Parameters

# Earth Parameters

earth_a = 1 * u.AU              # Semi-major axis in AU
earth_e = 0.01671123            # Eccentricity
earth_i = 0.00005 * u.deg       # Inclination in degrees
earth_w = 102.93768193 * u.deg  # Argument of perihelion in degrees
earth_OM = 0 * u.deg            # Longitude of ascending node in degrees

# Earth Parameters

# orbit_mars = Orbit.from_classical(Sun, mars_a, mars_e, mars_i, mars_w, mars_OM, vernal_equinox_date)
# orbit_earth = Orbit.from_classical(Sun, earth_a, earth_e, earth_i, earth_w, earth_OM, vernal_equinox_date)

# true_anomaly_earth = orbit_earth.true_anomaly
# true_anomaly_mars = orbit_mars.true_anomaly
# print(f"true_anomaly_earth {true_anomaly_earth}, true anomaly mars {true_anomaly_mars}")


launch_date = Time("2027-01-15")
radius_earth_orbit = 149.6 * 10**6
radius_mars_orbit = 227.9 * 10**6
per_day_earth_angular = 360/365.25
per_day_mars_angular = math.radians(360/687)

time_from_perihelion_to_equinox = (vernal_equinox_date - perihelion_earth).jd 
angle_from_perihelion_to_equinox = time_from_perihelion_to_equinox * per_day_earth_angular
print(f"angle from perihelion to equinox {angle_from_perihelion_to_equinox}")

time_from_equinox_to_launch = (launch_date - vernal_equinox_date).jd
angle_from_equinox_to_launch = time_from_equinox_to_launch * per_day_earth_angular
print(f"angle from equinox to launch {angle_from_equinox_to_launch}")
total_angle = angle_from_perihelion_to_equinox + angle_from_equinox_to_launch
print(f"total angle {total_angle}")
true_anomaly_at_launch = total_angle - 360
print(true_anomaly_at_launch)
print(f"true anomaly {((launch_date - vernal_equinox_date).days) * per_day_earth_angular}")
true_anomaly_earth = per_day_earth_angular * (launch_date - vernal_equinox_date).days

earth_x_at_launch = radius_earth_orbit * math.cos(true_anomaly_earth)
earth_y_at_launch = radius_earth_orbit * math.sin(true_anomaly_earth)

print(earth_x_at_launch, earth_y_at_launch)
print(true_anomaly_earth)

def mean_anomaly(date_perhileon, launch_date, T):
    radians_per_day = math.pi * 2 / T
    return (launch_date - date_perhileon).days * radians_per_day

def eccentric_anomaly(mean_anomaly, e, E):
    return E - e * math.sin(E) - mean_anomaly

def bisection_method(eccentric_anomaly, a, b, tolerance, mean_anomaly, e):
    if (eccentric_anomaly(mean_anomaly, e, a) * eccentric_anomaly(mean_anomaly, e, b)) < 0:
        while (abs(a - b) / 2.0 > tolerance):
            E_new = float(a + b) / 2.0
            if (eccentric_anomaly(mean_anomaly, e, a) * eccentric_anomaly(mean_anomaly, e, E_new) < 0):
                b = E_new
            else:
                a = E_new
    else:
        raise ValueError("Solution lies outside of guessed range.")
    return float(a + b) / 2.0

def true_anomaly(e, E):
    return math.arctan(math.sqrt(1 - e ** 2) * math.sin(E) / (math.cos(E) - e))

def distance_to_sun(a, b, e, E):
    return math.sqrt(b **2 * math.sin(E) ** 2 + a ** 2 * E ** 2 * math.cos(E) ** 2 - a ** 2 * e ** 2)

eccentric_anomaly_earth = eccentric_anomaly(mean_anomaly_earth, e_earth, E_earth)