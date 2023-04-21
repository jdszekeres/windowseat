from math import radians, sin, cos, atan2, sqrt, degrees, pow
import windowseat

def create_flight_path(start, end, start_bearing, end_bearing, num_points):
    # Calculate the distance and bearing between the two points
    lat1, lon1 = start
    lat2, lon2 = end
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = 1000 * 6371 * c  # convert distance to meters
    bearing = atan2(sin(dlon) * cos(radians(lat2)), cos(radians(lat1)) * sin(radians(lat2)) - sin(radians(lat1)) * cos(radians(lat2)) * cos(dlon))
    bearing = (degrees(bearing) + 360) % 360
    
    # Adjust the bearing for the runway headings
    bearing = (bearing + start_bearing) % 360
    end_bearing = (end_bearing + 180) % 360
    
    # Generate the flight path coordinates
    coords = []
    altitudes = []
    for i in range(num_points):
        frac = i / (num_points - 1)
        lat = lat1 + frac * (lat2 - lat1)
        lon = lon1 + frac * (lon2 - lon1)
        coords.append((lat, lon, bearing))
        bearing = (bearing + (end_bearing - start_bearing) / (num_points - 1)) % 360
        if i < num_points / 2:
            altitude = (36000 / (num_points / 2)) * i
        else:
            altitude = 36000 - (36000 / (num_points / 2)) * (i - num_points / 2)
        altitudes.append(altitude)
    altitudes.reverse()
    coords = [(coord[0], coord[1], coord[2], alt) for coord, alt in zip(coords, altitudes)]
    
    return coords



start = (39.99994, -82.887177)  # Colombus, OH
end = (40.641766, -73.780968)     # New York, NY
count = 20
flight_path = create_flight_path(start, end, 101,121,count)

for c,i in enumerate(flight_path):
    zoom_level = (-0.00007096758 * i[3] + 9.437068112) + 10
    windowseat.get_photo((i[1],i[0]),zoom_level,open("mapboxkey").read().splitlines()[0],i[2]+90,f"photos/{c}")

