import matplotlib.pyplot as plt
import numpy as np
from skyfield.api import load
from datetime import datetime

# Load ephemeris and timescale
eph = load('de421.bsp')
ts = load.timescale()

# Sun and planets
sun = eph['Sun']
earth = eph['Earth']
mars = eph['Mars']

# Define the launch date
launch_date = ts.utc(2027, 1, 15)  # Launch date is 2027-01-15

# Time range for Earth and Mars perihelion search (2026 and 2027)
t0 = ts.utc(2026, 1, 1)  # Start searching from 2026
t1 = ts.utc(2027, 1, 15)  # Stop at launch date
times = ts.linspace(t0, t1, 2000)  # More points to see the data more clearly

# Calculate Earth and Mars distances from the Sun
earth_distances = [np.linalg.norm(earth.at(t).position.km - sun.at(t).position.km) for t in times]
mars_distances = [np.linalg.norm(mars.at(t).position.km - sun.at(t).position.km) for t in times]

# Find the latest perihelion before the launch date for Earth and Mars
earth_perihelion_idx = np.argmin(earth_distances)  # Min distance is perihelion
mars_perihelion_idx = np.argmin(mars_distances)

# Get the times and dates of perihelion
earth_perihelion_time = times[earth_perihelion_idx]
mars_perihelion_time = times[mars_perihelion_idx]

earth_perihelion_date = earth_perihelion_time.utc_iso()
mars_perihelion_date = mars_perihelion_time.utc_iso()

# Calculate the time difference between launch date and perihelion dates for Earth and Mars
earth_perihelion_diff = abs(earth_perihelion_time - launch_date)
mars_perihelion_diff = abs(mars_perihelion_time - launch_date)

# Find which perihelion is closest to the launch date
if earth_perihelion_diff < mars_perihelion_diff:
    closest_perihelion_time = earth_perihelion_time
    closest_perihelion_distance = earth_distances[earth_perihelion_idx]
    closest_planet = 'Earth'
else:
    closest_perihelion_time = mars_perihelion_time
    closest_perihelion_distance = mars_distances[mars_perihelion_idx]
    closest_planet = 'Mars'

# Plot Earth and Mars distances from the Sun
plt.figure(figsize=(12, 6))

# Plot Earth
plt.plot([t.utc_datetime() for t in times], earth_distances, label="Earth-Sun Distance", color='blue')
plt.scatter(earth_perihelion_time.utc_datetime(), earth_distances[earth_perihelion_idx], color='blue', label='Earth Perihelion')
plt.annotate(f'Earth Perihelion\n{earth_perihelion_date}',
             xy=(earth_perihelion_time.utc_datetime(), earth_distances[earth_perihelion_idx]),
             xytext=(earth_perihelion_time.utc_datetime(), earth_distances[earth_perihelion_idx] + 1e7),
             arrowprops=dict(arrowstyle='->', color='blue'),
             fontsize=10, color='blue')

# Plot Mars
plt.plot([t.utc_datetime() for t in times], mars_distances, label="Mars-Sun Distance", color='orange')
plt.scatter(mars_perihelion_time.utc_datetime(), mars_distances[mars_perihelion_idx], color='orange', label='Mars Perihelion')
plt.annotate(f'Mars Perihelion\n{mars_perihelion_date}',
             xy=(mars_perihelion_time.utc_datetime(), mars_distances[mars_perihelion_idx]),
             xytext=(mars_perihelion_time.utc_datetime(), mars_distances[mars_perihelion_idx] + 1e7),
             arrowprops=dict(arrowstyle='->', color='orange'),
             fontsize=10, color='orange')

# Highlight the perihelion nearest to the launch date
plt.scatter(closest_perihelion_time.utc_datetime(), closest_perihelion_distance, color='red', label=f'{closest_planet} Perihelion Nearest to Launch')
plt.annotate(f'{closest_planet} Perihelion\n{closest_perihelion_time.utc_iso()}',
             xy=(closest_perihelion_time.utc_datetime(), closest_perihelion_distance),
             xytext=(closest_perihelion_time.utc_datetime(), closest_perihelion_distance + 1e7),
             arrowprops=dict(arrowstyle='->', color='red'),
             fontsize=10, color='red')

# Labeling and formatting
plt.xlabel('Date')
plt.ylabel('Distance (km)')
plt.title('Earth and Mars Distance from Sun (Latest Perihelion Before 2027-01-15)')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save the plot as an image
plt.savefig("latest_perihelions_before_launch_2027.png", dpi=300)
plt.show()

# Print the nearest perihelion information
print(f"Plot saved as latest_perihelions_before_launch_2027.png")
print(f"Nearest Perihelion to Launch: {closest_planet} Perihelion")
print(f"Perihelion Date: {closest_perihelion_time.utc_iso()}")