from math import radians, sin, cos, atan2, sqrt, degrees, pow
import windowseat
import re, requests
import sys
from math import atan2, degrees
import threading
from subprocess import run

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

def get_airport_info(airport,endport):
    # Construct the URL for the airport's AirNav page
    url = f"https://www.airnav.com/airport/{airport}"
    
    # Make a GET request to the URL and extract the page content
    response = requests.get(url)
    content = response.content.decode("utf-8")
    
    # Extract the latitude and longitude from the page content
    start,end = windowseat.get_db(airport,endport)
    
    # Use regex to find all instances of "x magnetic, y true"
    heading_pattern = r"(\d+) magnetic, (\d+) true"
    heading_matches = re.findall(heading_pattern, content)
    
    # Extract the true headings from the matches
    true_heading_start = [int(match[1]) for match in heading_matches][0]
    
    url = f"https://www.airnav.com/airport/{endport}"
    response = requests.get(url)
    content = response.content.decode("utf-8")
    heading_pattern = r"(\d+) magnetic, (\d+) true"
    heading_matches = re.findall(heading_pattern, content)
    
    # Extract the true headings from the matches
    true_heading_end = [int(match[1]) for match in heading_matches][0]
    # Make a GET request to the URL and extract the page content


    
    # Return a dictionary with the latitude, longitude, and true headings
    airport_info = {
        "start": start,
        "end": end,
        "true_headings": [true_heading_start,true_heading_end]
    }
    return airport_info


ainfo = get_airport_info(sys.argv[1], sys.argv[2])
print(ainfo)
start = ainfo["start"][::-1]
end = ainfo["end"][::-1]
time = int(sys.argv[3])
fps = int(sys.argv[4])
left = "l" in sys.argv[5]
count = time * fps
flight_path = create_flight_path(start, end, 101,121,count)
bearing_addition = 90
if left:
    bearing_addition -= 180
threads = []
for c,i in enumerate(flight_path):
    zoom_level = 17-((i[3]/36000)*5)
    # f.write(f"{c}, {zoom_level}\n")
    t = threading.Thread(target=windowseat.get_photo, args=((i[1],i[0]),zoom_level,open("mapboxkey").read().splitlines()[0],i[2]+bearing_addition,f"photos/{c:04n}"))
    threads.append(t)
    t.start()
for t in threads:
    t.join()

code = run(f"ffmpeg -framerate {fps} -i 'photos/%04d.jpg' flight.mp4; rm photos/*.jpg".split(" "))
if code.returncode != 0:
    print(f"command 'ffmpeg -framerate {fps} -i 'photos/%04d.jpg' flight.mp4; rm photos/*.jpg' returned an non-zero return code. Make sure you have ffmpeg installed.")
