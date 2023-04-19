import requests
import shutil
import numpy as np
import os
from math import atan2, degrees
import threading

def get_photo(center, zoom, key, bearing, loc):
    # Define the download URL
    url = f"https://api.mapbox.com/styles/v1/yopo/clgn5udy3001u01pl40l05mwj/static/{center[0]},{center[1]},{zoom},{bearing},60/480x640?access_token={key}"
    # Download the image
    response = requests.get(url, stream=True)
    with open('{}.jpg'.format(loc), 'wb') as f:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, f)
def get_points_on_line(coord1, coord2, count):
    x1, y1 = coord1
    x2, y2 = coord2
    dx = (x2 - x1) / (count - 1)
    dy = (y2 - y1) / (count - 1)
    points_on_line = [(x1 + i*dx, y1 + i*dy) for i in range(count)]
    return points_on_line
def get_angle_between_coordinates(coord1, coord2):
    # Get latitude and longitude differences between coordinates
    delta_lat = coord2[0] - coord1[0]
    delta_lon = coord2[1] - coord1[1]
    
    # Calculate the angle in radians using atan2
    angle = atan2(delta_lat, delta_lon)
    
    # Convert angle from radians to degrees
    angle_degrees = degrees(angle)
    
    # Ensure angle is between 0 and 360 degrees
    if angle_degrees < 0:
        angle_degrees += 360
        
    return angle_degrees

# Define the area of interest
start_1 = (32.7317,-117.19)
end_1 = ( 40.76078, -111.89105)
#invert for mapbox
start = start_1[::-1]
end = end_1[::-1]
time = 30 # in secs
fps = 30 #fps
count = fps * time
zoom=10.5
key = "pk.eyJ1IjoieW9wbyIsImEiOiJjbDA0bzhoM2EwMWhiM2NxajV2Zm1lYmpyIn0.kL4KlQH8tl89C6dJtL31gw"
pol = get_points_on_line(start,end,count)
bearing = get_angle_between_coordinates(start_1,end_1)+90
threads = []
# Start a thread for each photo download
for i, v in enumerate(pol):
    filename = f"photos/{i:04n}"
    t = threading.Thread(target=get_photo, args=(v, zoom, key, bearing, filename))
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()
print("call this function to stitch files together:")
print(f"ffmpeg -framerate {fps} -i 'photos/%04d.jpg' flight.mp4")