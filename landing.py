import windowseat
import numpy as np
import random
import math

def calculate_new_coordinate(lat, lon, heading, distance):
    """
    Calculate a new coordinate given an original coordinate, heading, and distance.
    
    Parameters:
        lat (float): The original latitude coordinate in decimal degrees.
        lon (float): The original longitude coordinate in decimal degrees.
        heading (float): The heading in degrees from north (0 degrees) clockwise (0 to 360 degrees).
        distance (float): The distance in kilometers.
    
    Returns:
        A tuple containing the new latitude and longitude coordinates in decimal degrees.
    """
    # Convert latitude and longitude to radians
    lat = math.radians(lat)
    lon = math.radians(lon)
    
    # Convert heading to radians
    heading = math.radians(heading)
    
    # Convert distance to radians (angular distance)
    distance = distance / 6371.0  # Earth's radius in kilometers
    
    # Calculate new latitude and longitude coordinates
    new_lat = math.asin(math.sin(lat) * math.cos(distance) + math.cos(lat) * math.sin(distance) * math.cos(heading))
    new_lon = lon + math.atan2(math.sin(heading) * math.sin(distance) * math.cos(lat), math.cos(distance) - math.sin(lat) * math.sin(new_lat))
    
    # Convert new latitude and longitude to decimal degrees
    new_lat = math.degrees(new_lat)
    new_lon = math.degrees(new_lon)
    
    # Return new coordinate as a tuple
    return (new_lat, new_lon)



airplane_runway = 90
interval = 20

airport = (32.671993, -117.022305)[::-1]
endloc = calculate_new_coordinate(airport[1],airport[0],airplane_runway,5)[::-1]
alt_end = 15
alt_start = 17
points = windowseat.get_points_on_line(airport,endloc,interval)
print(endloc)
zooms = np.linspace(alt_start,alt_end,interval)
key = random.choice(open("mapboxkey").read().splitlines())
for i, v in enumerate(points):
    windowseat.get_photo(v,zooms[i],key,90+airplane_runway,f"photos/{i:04n}")


